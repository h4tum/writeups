# Writeup: rcaas (BYUCTF 2026)

- **Event:** [BYUCTF 2026](https://chals.cyberjousting.com) ([CTFTime](https://ctftime.org/event/3247/))
- **Challenge:** rcaas
- **Category:** Reverse Engineering
- **Solved by:** [dopri](https://github.com/DoPri/)

We are given `rcaas`, a Go binary compiled with debug info (not stripped), and a partial disassembly excerpt in `run.asm` showing the core of `main.(*program).run`.

## Initial Analysis

The program reads a file from disk (path built with `filepath.Join`), splits the contents on whitespace, and validates the first token as a filename ending in `.asm`. It then checks that the file length is at least `0x22` bytes and runs a long series of constraints on individual bytes.

From `run.asm` and the decompiled logic:

- The input must start with the seven-byte prefix `byuctf{` (checked via string comparison and explicit prefix constraints in the solver).
- The total length is 46 bytes, with `}` at index 45.
- Several indices are forced to the character `'3'` (indices 13, 21, 24, 26, 29, 31, 36, 37, 39 in the solver script).
- Indices 0x0d through 0x27 (in a loop in the assembly) must each equal `0x33` (`'3'`), which matches the fixed `'3'` positions above.
- Twenty-eight additional checks multiply two bytes (as 8-bit values) and compare the product to a constant (for example `file[34] * file[1] == 41`, `file[40] * file[4] == 80`, and so on). These are the usual "reverse as a system of equations" pattern.
- Near the success path, two bytes must be `>= 0x60` (lowercase ASCII), which the solver encodes by restricting characters to `[a-z0-9_{}]`.

Because multiplication is modulo 256, some equations admit multiple solutions for a given byte. The solver pins `file[20]` to `'b'` explicitly after noticing that another value could also satisfy the modular product for part of the interior string.

## Solution

`solve.py` models each flag byte as a 32-bit bitvector, adds the format and character-set constraints, adds all product equations extracted from the assembly, and calls Z3's `check()`. On `sat`, it prints the unique satisfying assignment.

The recovered plaintext is 46 characters, starts with `byuctf{`, ends with `}`, and satisfies every check in `run.asm`. Running the script locally:

```bash
cd rcaas && uv run python solve.py
```

No network interaction is present in the challenge files; this is an offline reverse-and-constraint-solving task.
