Writeup CO-OP Box
===

- Category: pwn
- Final point value: 500
- Number of solves: 1
- Solved by: fkil

## Challenge Description

[Andy Nguyen](https://x.com/theflow0) found a really nice bug for VirtualBox and even wrote a [PoC](https://github.com/google/security-research/tree/master/pocs/oracle/virtualbox/cve-2023-22098), unfortunately it is only for linux. Can you port it to Windows? All relevant files are in the zip and it includes a README with more infos about the setup.

## Overview

We need to exploit a VirtualBox CVE that has a PoC for linux and need to port it to Windows. The Windows binaries are from a debug build (with debug symbols). The PoC consists of only code without an accompanying writeup, thus the first step will be to analyze the vulnerability and PoC. Afterwards, we can look at the differences for Windows and how to exploit there.


## The vulnerability

From the [security advisory](https://github.com/google/security-research/security/advisories/GHSA-q7p4-pxjx-6h42), we can extract the following:

In the `VIRTIONET_CTRL_VLAN` the bounds-check for the `uVlanId` is inverted, thus we can set/clear bits out-of-bounds (but not in-bounds).

## Analysis of Linux PoC

As the `uVlanId` is a 16-bit integer, we have a bounded relative arbitrary write primitive. To get to RCE, a leak and a function pointer overwrite will be necessary. We will discuss them in this order, but first start by discussing relevant structures and their allocation.

### VirtualBox device structures

The PoC is making use of the device structures of VirtualBox. The `virtio-net` device is a device registered through VirtualBox's Pluggable Device Manager (PDM), so let's take a look at its structures and their allocation. 

When PDM devices are initialized in `pdmR3DevInit` of `VBOX/VMM/VMMR3/PDMDevice.cpp`, the ring-3 (`R3`/user-space) component will go through the list of registered devices and for each device perform the allocation via a hypercall to the ring-0 (`R0`/kernel-space) component. The allocation routine in `R0` will allocate a memory object for the following data (taken from `VBox/VMM/VMMR0/PDMR0Device.cpp`):

```
--------------------------------------
ring-0 devins
--------------------------------------
ring-0 instance data
--------------------------------------
ring-0 PCI device data (optional) ??
--------------------------------------
page alignment padding
--------------------------------------
ring-3 devins
--------------------------------------
ring-3 instance data
--------------------------------------
ring-3 PCI device data (optional) ?? 
--------------------------------------
[page alignment padding                ] -
[--------------------------------------]  \
[raw-mode devins                       ]   \
[--------------------------------------]   - Optional, only when raw-mode is enabled.
[raw-mode instance data                ]   /
[--------------------------------------]  /
[raw-mode PCI device data (optional)?? ] -
--------------------------------------
shared instance data
--------------------------------------
default crit section
--------------------------------------
shared PCI device data (optional)
--------------------------------------

```

The `R0` component will then do much of the initialization and map the `R3` and shared data into the `R3` process. Afterwards, the `R3` component will call the device's `Construct` routine to finish initialization.

For the PoC, the `R3` and shared PCI data is of interest. The **dev**ice **ins**tance data corresponds to `PDMDEVINSR3`, the instance data for the `virtio-net` device corresponds to `VIRTIONET` and contains the bitmap to which we have a relative write. Finally, the device is connected via a virtual PCI and its shared data corresponds to an instance of `PDMPCIDEV`.

As such, the data we can consistently access with the vulnerability is the shared instance data, default critical section and the shared PCI device data.

### Getting a leak primitive

PCI devices have a configuration space that can be read from and written to. If one can somehow modify the pointer from where data is read, we could abuse it to read data and leak pointers. In the implementation of the config space read, an indirect call using the `pfnConfigRead` field of the `PCMPCIDEV` structure is performed. 

For `virtio-net` this field is set to `virtioR3PciConfigRead`, which is inside the `VBoxDD` library. Let's look at what the PCI config read implementation does (`virtioR3PciConfigRead` in `VBox/Devices/VirtIO/VirtioCore.cpp`):

 - First `pDevInsR3` from the internal data of the `PDMPCIDEV` (which is under our control) is used to get a pointer to `PDMDEVINS` struct.
 - Then, the `pInstanceData` field from `pDevInsR3` is read to get a pointer (`pVirtio`) to the `VIRTIOCORE` structure (which is the first field inside of `VIRTIONET`). And `pVirtioCC` (the current-context instance data, which will also be the `R3` instance data) is computed by offsetting from `pDevInsR3` (Remember, the device-specific instance data is directly after the generic device instance data).
 - `pPciCfgCap` is read from `pVirtioCC` to retrieve a pointer (`pPciCap`) to the config area. This points inside the `abConfig` field of the `PDMPCIDEV` structure
 - the offset and length is read from `pPciCfgCap` (these values would be set by the guest driver beforehand). Then it verifies that the length is either 1, 2 or 4 and `pPciCap->uBar` is equal to `VIRTIO_REGION_PCI_CAP`.
 - Then, given the offset, the correct field is searched inside `pVirtIo`. For this, there are multiple fields inside `VIRTIOCORE` with the naming scheme `LocXCfg` that contain start and end offsets.
     - Here, the most convenient area is the `Common` area as the other options will either directly overwrite what we read or have an indirect call.
     - For the `Common` config the offset is then directly mapped to the corresponding field. Most fields don't have additional access logic and will just return the value of the field.

Now that we know how the config read is implemented, how can we exploit it? We cannot directly fake a `pDevInsR3` structure as we don't have any memory leak yet and `pInstanceData` and `pPciCfgCap` would need to be set as well. The PoC solves this by shifting the `pDevInsR3` pointer so that these pointers are read from different fields and a type-confusion occurs. 

Specifically, if we shift it by 0x10, `pInstanceData` will be read from `pCritSectRoR3` and `pPciCfgCap` from `pCommonCfgCap`. The `pCritSectRoR3` is also after the bitmap, thus we can write arbitrary data in it and fake a `VIRTIOCORE` structure.

Furthermore, the config fields of the fake `VIRTIOCORE` will contain the shared PCI data (`PDMPCIDEV`), thus we can leak values from it. From the documentation, the critical section is only used for power off, power on, suspend and resume, thus we do not have to worry that our corruption there would crash something.

The `pCommonCfgCap` points inside the shared PCI device config - like `pPciCfgCap` - and thus is also under our control. As such, we set the aforementioned `LocXCfg` variables in the fake `VIRTIOCORE` struct and the fake `pPciCfgCap` values to specify which configuration value we want to read.

Using this, the PoC then leaks the following values from the internal data of `PDMPCIDEV`:
 - `pDevInsR3` pointing to the area of the device data, now allowing us to fake pointers to the area where we have control
 - `pfnConfigRead` pointing to the `virtioR3PciConfigRead` function giving us a pointer to the `VBoxDD` that contains many gadgets

Both values are contained inside the config data for `aVirtQueues[4]`, thus the PoC has a helper function setting up a read from `aVirtQueues[4]`, which requires also setting the `uVirtQSelect` inside the fake `VIRTIOCORE` struct to `4`.

### Getting RCE in Linux

The PoC proceeds by writing a ROP and shellcode into the device data area and relocating the stack to the ROP payload by overwriting `pfnConfigRead` and `pDevIns`. The ROP does the following:

 - Load `RTQueryFileSize` (located in `VBoxRT`) from the `GOT` of `VBoxDD`
 - Add an offset to get a pointer to `RTMemProtect` (also located in `VBoxRT`)
 - Call `RTMemProtect` to make the shellcode executable
 - Jump into shellcode

## Porting to Windows

The bug and the general logic how to get an initial leak can be easily ported to Windows. We just need to modify the defined offsets of the structs in the PoC. To get the correct offsets, we used `WinDBG`, set a breakpoint to `virtioR3PciConfigRead` and read out the values from the device instance structure. This already allows us to also get a leak to `VBoxDD` and the memory area of the device data.

### RCE in Windows

The binary is compiled with Windows' `ControlFlowGuard` protection, thus we cannot overwrite `pfnConfigRead` to an arbitrary gadget to start a ROP chain and need to find a different way. Without going into too much depth, `ControlFlowGuard` makes sure that each indirect call target is a beginning of a defined function. Thus, while we cannot overwrite it to a gadget, we can overwrite it to an arbitrary function!

Let's take a closer look at the first two arguments that will be passed to `pfnConfigRead`:
 1. value of `pDevInsR3` from the internal `PDMPCIDEV` data (which we have full control over)
 2. a pointer to the `PDMPCIDEV` structure (which we can read/write data from)

The final goal of the challenge was to call `calc.exe`, thus we would optimally set `pfnConfigRead` to `WinExec` and `pDevInsR3` to a pointer to `"calc.exe"`. However, we do not know the location of `WinExec`/`kernel32.dll` and inside the device memory area there is no pointer to `kernel32.dll` that we can leak yet.

As such, we need to somehow build an arbitrary read gadget and then we could leak a `kernel32.dll` address from the Import Address Table (`IAT`) of `VBoxDD.dll`.

### Getting an arbitrary read primitive

We can call arbitrary functions in `VBoxDD` by overwriting `pfnConfigRead`. As mentioned, we can fully control the first argument and the second argument points to an area under our control. However, we cannot get the return value as it will be interpreted as an internal error code of VirtualBox. Therefore, the return value should optimally be `0`/`VINF_SUCCESS`.

Our optimal function thus should:
 - not call any other function
 - read a value from an offset to `arg1`
 - write this value to an offset to `arg2`
 - return 0

`VBoxDD.dll` is pretty big, so there are good chances to find such a function. We used `BinaryNinja` and exported the decompiled code for all functions inside the `VBoxDD.dll` binary. Then, via regex search we looked for functions that fulfilled the following properties and found the following function:

```cpp
18006a3f0  int64_t sub_18006a3f0(void* arg1, int64_t arg2)

18006a3f0  {
18006a3f0      int64_t r9;
18006a3f0      arg_20 = r9;
18006a3f5      char r8;
18006a3f5      arg_18 = r8;
18006a41f      *(uint8_t*)(arg2 + 0xc) = *(uint8_t*)((char*)arg1 + 0xf1);
18006a423      int64_t rax;
18006a423      rax = 0;
18006a426      return 0;
18006a3f0  }
```

This function will read a single byte from `arg1 + 0xf1` and write it to `arg2+0xc`.

Thus, to leak an arbitrary byte from `ptr`, we do:

 - Set `pDevInsR3` of `PDMPCIDEV` to `ptr-0xf1`
 - Set `pfnConfigRead` to `sub_18006a3f0`
 - perform a PCI config read, triggering the call to `sub_18006a3f0`
 - Reset `pDevInsR3` and `pfnConfigRead` to their original values
 - With the initial leak gadget leak the byte from `PDMPCIDEV + 0xc`
     - To get the correct field to read, one can inspect the fake `VIRTIO` via `WinDbg` and see which field this corresponds to
     - For us, this was the high word of `aVirtQueues[2].GCPhysVirtqUsed`, thus we read `VIRTIO_PCI_COMMON_Q_USEDHI`

### Putting everything together

With our arbitrary read gadget we now can leak a `kernel32.dll` address and get the address of `WinExec`. There are many options, and we opted to leak the address of `CloseHandle` from the `IAT`.

Next, we simply had to write the payload string `"calc.exe"` inside the device data area, overwrite `pfnConfigRead` to `WinExec` and `pDevInsR3` to the address of our payload string and issue a PCI config read to spawn a calculator.

