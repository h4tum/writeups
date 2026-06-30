# Writeup: yara (BYUCTF 2026)

- **Event:** [BYUCTF 2026](https://chals.cyberjousting.com) ([CTFTime](https://ctftime.org/event/3247/))
- **Challenge:** yara
- **Category:** Reverse Engineering
- **Solved by:** [dopri](https://github.com/DoPri/)

We are given `rule.yar`, a YARA rule named `fleg`, and `solve.py`, which reconstructs the matching string. There is no separate binary; the challenge is to find a byte sequence that satisfies every clause in the rule.

## Initial Analysis

The rule defines many string patterns and requires `all of them` plus three integer comparisons at fixed offsets:

| Condition | Meaning |
|-----------|---------|
| `$c = /byuctf.{33}/` | Starts with `byuctf{`, 33 characters inside braces, 39 bytes total |
| `uint32(21) == 0x6E347473` | Little-endian dword at offset 21 is `st4n` |
| `uint16(28) == 0x7230` | Little-endian word at offset 28 is `0r` |
| `uint16be(29) == 0x725F` | Big-endian word at offset 29 is `r_` |

Individual strings pin down fragments:

- `$i = { 7B 77 }` fixes `{w` at offset 6 (overlapping the opening brace from `$c`).
- `$d = { 77 ?8 79 }` gives `why` at offsets 7–9.
- `$k`, `$m`, `$a`, `$f`, `$q`, `$l`, `$b`, `$p`, `$e`, `$g`, `$j` constrain further slices with hex wildcards, literal `yara`, base64 decoding of `do3s`, and XOR decoding of `th4t?`.
- Comments in the rule file document the intended ASCII for some XOR/base64 strings (for example `do3s` and `th4t?`).

The wildcards (`?`) leave individual nibbles or bytes unknown until other constraints overlap the same offsets.

## Solution

`solve.py` builds a 39-byte `bytearray` and fills it slice by slice as each rule fragment is resolved. Overlapping constraints must agree (for example `$k` and `$m` both influence the `hy_d` region). The script prints the completed string when every pattern and integer check is satisfied.

This is manual constraint propagation rather than running YARA against a corpus: the rule *is* the specification of the flag format.

Running locally:

```bash
cd yara && python solve.py
```

The output is the unique string that satisfies `rule fleg` under the given wildcards and endianness checks.
