# Writeup: Zenmaster (WHY2025 CTF)

- **Event:** [WHY2025 CTF](https://ctf.why2025.org/) ([CTFTime](https://ctftime.org/event/2680))
- **Challenge:** Zenmaster
- **Category:** Reverse Engineering
- **Solved by:** [dopri](https://github.com/DoPri/)

We are provided with an AMD microcode update file named `cpu008A0F00_ver08A000FF.bin`. The challenge infrastructure allowed us to upload an ELF file and receive its user-mode output, suggesting we needed to trigger specific CPU behavior modified by this microcode.

## Initial Analysis

My analysis began with [MCExtractor](https://github.com/platomav/MCExtractor), a tool used to parse and validate microcode binaries. This provided general information about the file structure and confirmed it was a valid AMD microcode update.

To dive deeper, I utilized Zentool, a utility developed by Google for researching the AMD Zen microarchitecture. I was familiar with this tool from previous security research and relied on the following documentation:

- [Blog Post](https://bughunters.google.com/blog/5424842357473280/zen-and-the-art-of-microcode-hacking)
- [Zentool Intro](https://github.com/google/security-research/blob/master/pocs/cpus/entrysign/zentool/docs/intro.md)
- [Zentool/RISC86 Reference](https://github.com/google/security-research/blob/master/pocs/cpus/entrysign/zentool/docs/reference.md)

To better understand the RISC86 microarchitecture and the inner workings of the CPU, I consulted the seemingly only authoritative text [The Anatomy of a High-Performance Microprocessor: A Systems Perspective (ISBN 0818684003)](https://archive.org/details/anatomyofhighper0000shri). I also reviewed patent filings **US5926642A** and **US006336178B1** for additional context on the underlying technology.

## Microcode Patch Extraction

Using `zentool`, I extracted the specific microcode patches contained within the binary. The output revealed that all patches targeted the `fpatan` instruction. This choice is significant as `fpatan` is rarely used in modern software, making it a common target for demonstrating microcode updates (as seen in Google's own documentation).

The `zentool` output provided the following disassembly of the patch:

```text
Date:        07112025 (Fri Jul 11 2025)
Revision:    08a000ff
Format:      8004
Patchlen:    00
Init:        00
Checksum:    00000000
NorthBridge: 0000:0000
SouthBridge: 0000:0000
Cpuid:       00008a00 AMD Ryzen (Mendocino)
  Stepping   0
  Model:     0
  Extmodel:  10
  Extfam:    8
BiosRev:     00
Flags:       00
Reserved:    0000
Signature:   7e... (use --verbose to see) (GOOD)
Modulus:     80... (use --verbose to see)
Check:       17... (use --verbose to see) (GOOD)
Autorun:     false
Encrypted:   false
Revision:    08a000ff (Signed)
; Patch 0x8a000ff Match Registers (44 total)
; (use --verbose to see empty slots)
	[0 ] 0CE0 @fpatan
; Patch 0x8a000ff OpQuad Disassembly (64 total)
; (use --verbose to see further details)
.quad  0, 0x00000001	; @0x1fc0
	mov     	reg15, reg15, rax
	mov     	reg14, reg14, 0x907f
	shl     	reg14, reg14, 0x000c
	add     	reg14, reg14, 0x01a9
.quad  1, 0x00000001	; @0x1fc1
	sub     	reg0, reg0, reg14
	ld.p    	7:[reg0+0x3d2], reg0
	mov     	rax, reg0, 0x0041
	mov     	rbx, reg0, 0xf1a9
.quad  2, 0x00000001	; @0x1fc2
	shl     	rbx, rbx, 0x0010
	mov     	reg15, reg15, 0x6761
	shl     	reg15, reg15, 0x0010
	add     	reg15, reg15, 0x6c66
.quad  3, 0x00000001	; @0x1fc3
	.dq     	0x18505c07cc079800 ; Unhandled Class 3
	add     	rbx, rbx, 0x0004
	mov     	reg15, reg15, 0x007b
	.dq     	0x18505c07cc079800 ; Unhandled Class 3
.quad  4, 0x00000001	; @0x1fc4
	add     	rbx, rbx, 0x0001
	mov     	reg14, reg14, 0x4257
	ld      	reg13, ms:[reg14+reg0]
	mov     	reg15, reg15, 0x3a1b
.quad  5, 0x00000001	; @0x1fc5
	shl     	reg15, reg15, 0x0010
	add     	reg15, reg15, 0xd1d0
	xor     	reg15, reg15, reg13
	.dq     	0x18505c07cc079800 ; Unhandled Class 3
.quad  6, 0x00000001	; @0x1fc6
	add     	rbx, rbx, 0x0004
	mov     	reg15, reg15, 0x6a4f
	shl     	reg15, reg15, 0x0010
	add     	reg15, reg15, 0x82d3
.quad  7, 0x00000001	; @0x1fc7
	xor     	reg15, reg15, reg13
	.dq     	0x18505c07cc079800 ; Unhandled Class 3
	add     	rbx, rbx, 0x0004
	mov     	reg15, reg15, 0x6a18
.quad  8, 0x00000001	; @0x1fc8
	shl     	reg15, reg15, 0x0010
	add     	reg15, reg15, 0x8583
	xor     	reg15, reg15, reg13
	.dq     	0x18505c07cc079800 ; Unhandled Class 3
.quad  9, 0x00000001	; @0x1fc9
	add     	rbx, rbx, 0x0004
	mov     	reg15, reg15, 0x6f14
	shl     	reg15, reg15, 0x0010
	add     	reg15, reg15, 0x8381
.quad 10, 0x00000001	; @0x1fca
	xor     	reg15, reg15, reg13
	.dq     	0x18505c07cc079800 ; Unhandled Class 3
	add     	rbx, rbx, 0x0004
	mov     	reg15, reg15, 0x6f4e
.quad 11, 0x00000001	; @0x1fcb
	shl     	reg15, reg15, 0x0010
	add     	reg15, reg15, 0x83d3
	xor     	reg15, reg15, reg13
	.dq     	0x18505c07cc079800 ; Unhandled Class 3
.quad 12, 0x00000001	; @0x1fcc
	add     	rbx, rbx, 0x0004
	mov     	reg15, reg15, 0x694d
	shl     	reg15, reg15, 0x0010
	add     	reg15, reg15, 0x86d0
.quad 13, 0x00000001	; @0x1fcd
	xor     	reg15, reg15, reg13
	.dq     	0x18505c07cc079800 ; Unhandled Class 3
	add     	rbx, rbx, 0x0004
	mov     	reg15, reg15, 0x3d1f
.quad 14, 0x00000001	; @0x1fce
	shl     	reg15, reg15, 0x0010
	add     	reg15, reg15, 0x8cd2
	xor     	reg15, reg15, reg13
	.dq     	0x18505c07cc079800 ; Unhandled Class 3
.quad 15, 0x00000001	; @0x1fcf
	add     	rbx, rbx, 0x0004
	mov     	reg15, reg15, 0x6d1b
	shl     	reg15, reg15, 0xd0d1
.quad 16, 0x00000001	; @0x1fd0
	xor     	reg15, reg15, reg13
	.dq     	0x18505c07cc079800 ; Unhandled Class 3
	add     	rbx, rbx, 0x0004
	mov     	reg15, reg15, 0x007d
.quad 17, 0x00000001	; @0x1fd1
	.dq     	0x18505c07cc079800 ; Unhandled Class 3
	<bad>   	reg0, reg0, reg0
	<bad>   	reg0, reg0, reg0
	<bad>   	reg0, reg0, reg0
```

Upon reviewing this output, I noticed a pattern suggesting a XOR cipher utilizing a fixed 32-bit key. Specifically, below `.quad 2`, the values `0x6761` and `0x6c66` are moved into registers. When reversed, the sequence `66 6C 61 67` corresponds to the ASCII string "flag", implying that the flag was encoded directly within the microcode update itself.

## Solution

_Disclaimer:_ The way I solved it was probably not the way it was intended. I assume the intended solution involved crafting an ELF file to execute the `fpatan` instruction and retrieve the flag via the patched behavior. I attempted this briefly but struggled with the x87/FPU-style assembly and the opaque nature of the RISC86 code (specifically the confusing "Unhandled Class" `.dq` directives, which I eventually ignored).

Recognizing that the encryption key was only 32 bits long, I opted to brute-force it. I extracted the ciphertext from the update file. I constrained the search space by validating that the decrypted output must consist of lowercase letters `a-f` and numbers (matching the hex format of the flag), be exactly 32 characters long, and be wrapped in `flag{...}`.

I wrote the following Python script to perform a multithreaded brute-force attack on the key:

```python
import json
import multiprocessing
import os
import time

obfuscated_data = [
    0x3A1BD1D0,
    0x6A4F82D3,
    0x6A188583,
    0x6F148381,
    0x6F4E83D3,
    0x694D86D0,
    0x3D1F8CD2,
    0x6D1BD0D1,
]


def decode_flag(key: int) -> str:
    flag = "flag{"

    for data in obfuscated_data:
        decrypted_dword = data ^ key
        flag += decrypted_dword.to_bytes(4, byteorder="little").decode("ascii")

    flag += "}"

    return flag


def is_valid_char_code(code: int) -> bool:
    is_digit = (code >= ord("0")) and (code <= ord("9"))
    is_lower = (code >= ord("a")) and (code <= ord("f"))
    return is_digit or is_lower


def solve_for_key():
    print("Starting key search... This may take a minute.")

    flags: dict[int, str] = dict()

    for key in range(2**32):
        all_chunks_are_valid = True

        for data in obfuscated_data:
            decrypted_dword = data ^ key

            b1 = decrypted_dword & 0xFF
            b2 = (decrypted_dword >> 8) & 0xFF
            b3 = (decrypted_dword >> 16) & 0xFF
            b4 = (decrypted_dword >> 24) & 0xFF

            if not (is_valid_char_code(b1) and is_valid_char_code(b2) and is_valid_char_code(b3) and is_valid_char_code(b4)):
                all_chunks_are_valid = False
                break

        if all_chunks_are_valid:
            flag = decode_flag(key)
            print(f"Decryption Key (Hex): {hex(key)}, Flag: {flag}")
            flags[key] = flag

    print(f"Summary:\n{flags}")


def search_key_range(r: range) -> dict[int, str]:
    local_flags: dict[int, str] = {}

    for key in r:
        all_chunks_are_valid = True
        for data in obfuscated_data:
            decrypted_dword = data ^ key

            b1 = decrypted_dword & 0xFF
            b2 = (decrypted_dword >> 8) & 0xFF
            b3 = (decrypted_dword >> 16) & 0xFF
            b4 = (decrypted_dword >> 24) & 0xFF

            if not (is_valid_char_code(b1) and is_valid_char_code(b2) and is_valid_char_code(b3) and is_valid_char_code(b4)):
                all_chunks_are_valid = False
                break

        if all_chunks_are_valid:
            flag = decode_flag(key)
            print(f"Worker (PID: {os.getpid()}) found candidate Key: {hex(key)}, Flag: {flag}")
            local_flags[key] = flag

    return local_flags


def solve_for_key_multithreaded():
    num_processes = os.cpu_count() or 4
    print(f"Starting key search using {num_processes} parallel processes...")

    total_keys = 2**32
    chunk_size = total_keys // num_processes
    ranges: list[range] = []
    for i in range(num_processes):
        start = i * chunk_size
        end = (i + 1) * chunk_size
        # Ensure the last chunk covers the entire remaining range
        if i == num_processes - 1:
            end = total_keys
        ranges.append(range(start, end))

    start_time = time.time()

    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(search_key_range, ranges)

    all_flags: dict[int, str] = {}
    for result_dict in results:
        all_flags.update(result_dict)

    end_time = time.time()

    print(f"\nSearch completed in {end_time - start_time:.2f} seconds.")
    print(f"Summary of all found keys and flags:\n{json.dumps(all_flags, indent=2)}")


if __name__ == "__main__":
    solve_for_key_multithreaded()
```

## Results

Running this multithreaded brute-force script took approximately 5.5 minutes and yielded 64 possible flags. Fortunately, the correct flag was among the first 20 results.
