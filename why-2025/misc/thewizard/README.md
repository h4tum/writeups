# Writeup: The Wizard (WHY2025 CTF)

**Event:** [WHY2025 CTF](https://ctf.why2025.org/) ([CTFTime](https://ctftime.org/event/2680))
**Challenge:** The Wizard
**Category:** Misc
**Solved by:** [dopri](https://github.com/DoPri/)

We are provided with a collection of Linux configuration files (dotfiles).

## Initial Analysis

A quick inspection of the standard dotfiles (`.bashrc`, `.profile`, etc.) showed they are mostly default boilerplate. The outlier is `.pwfault`, which contains a large blob of seemingly random characters and noise.

My `decrypt.py` script is designed to process this specific file format, suggesting that `.pwfault` holds the obfuscated flag.

## Solution

I wrote `decrypt.py` based on the obfuscation logic I discovered in the `.viminfo` file:

1. The script reads the content of `.pwfault` and keeps only lines that contain a question mark (`?`).
2. From these filtered lines, it removes all characters except hexadecimal digits (`0-9`, `a-f`).
3. It joins the resulting hex strings and removes the substring "dd".
4. The remaining hex string is wrapped in `flag{...}`.

The script essentially filters out the noise to reveal the hex-encoded flag.

```python
lines_with_question_mark = [line for line in content.split("\n") if "?" in line]
hex_parts = [re.sub(r"[^a-f0-9]", "", line) for line in lines_with_question_mark]
hex_string = "".join(hex_parts).replace("dd", "")
```

Running the script against the provided `.pwfault` file to recover the flag.
