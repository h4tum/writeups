# Writeup: angr-management (BYUCTF 2026)

- **Event:** [BYUCTF 2026](https://chals.cyberjousting.com) ([CTFTime](https://ctftime.org/event/3247/))
- **Challenge:** angr-management
- **Category:** Reverse Engineering
- **Solved by:** [dopri](https://github.com/DoPri/)
- **Remote:** `chals.cyberjousting.com:1368`

The description says the author built a maze using `goto` statements and that we must navigate it successfully to receive the flag. The distributed `angr_management_test` binary contains a dummy flag; the real flag is on the remote instance. The note also mentions that angr could be used, which matches the challenge name.

## Initial Analysis

The binary is a PIE-enabled ELF with a very large `main` function implemented almost entirely as a control-flow graph of compares and jumps rather than structured loops. `objdump -d` output is saved in `objdump.txt` (over 12,000 lines of disassembly).

The program reads integers from stdin in a loop. At many basic blocks it compares the last input value (`DWORD PTR [rbp-0x4]`) against a constant and branches. Wrong choices lead to error messages and `exit(1)`; the success path eventually reaches the code that prints the real flag (around offset `0xedfe` relative to the binary base in the local dump).

Manually following hundreds of branches is impractical. Two approaches exist in this repository:

- `solve.py` uses angr symbolic execution with `simgr.explore(find=success_addr)` to discover stdin that reaches the success basic block.
- `parser.py` parses `objdump.txt`, builds a graph of `jmp` / `cmp`+`jne`/`je` edges, and runs BFS from `main` to the success address, collecting the sequence of comparison values that must be entered.

Both approaches converge on the same path. The BFS result is stored in `input.txt` (72 integers) and duplicated in `get_flag.py` for the remote.

## Solution

`parser.py` walks the disassembly starting at `<main>:` and stops before `<_fini>`. For each `cmp` against `[rbp-0x4]` followed by a conditional jump, it records which input value leads toward the success block versus the failure block. A breadth-first search from the entry address to `0xedfe` yields the ordered list of required inputs.

`get_flag.py` connects to `chals.cyberjousting.com:1368`, sends each number on its own line, and prints the server response.

The local test binary can be verified by piping `input.txt` into it:

```bash
cat input.txt | ./angr_management_test
```

I did not rely on angr for the final remote solve; the static graph extraction was faster.
