# Writeup: Keypad (WHY2025 CTF)

- **Event:** [WHY2025 CTF](https://ctf.why2025.org/) ([CTFTime](https://ctftime.org/event/2680))
- **Challenge:** Keypad
- **Category:** Forensics
- **Solved by:** [dopri](https://github.com/DoPri/)

We are provided with two images (`Keypad_1.jpg`, `Keypad_2.jpg`) and a Saleae Logic analyzer capture file (`Keypad.sal`).

## Initial Analysis

The images show the keypad and its wiring to the logic analyzer. The `.sal` file contains a recording of digital signals which can be viewed using the [Saleae Logic 2](https://saleae.com/downloads) software.

By inspecting the capture in the Logic software, I could see which lines of the keypad matrix were active at specific times. I manually transcribed these events into a text file named `raw.txt` to simplify the decoding process. The format I used for `raw.txt` is `column, row, count`.

Example from `raw.txt`:

```text
2,4,1
3,5,1
2,6,1
```

## Solution

I wrote a Python script `decode.py` to map these coordinates back to the characters on the keypad.

Based on the provided images and the logic analyzer data, I reconstructed the keypad matrix in the script:

```python
keypad_map = [
    ["1", "4", "7", "*"],
    ["2", "5", "8", "0"],
    ["3", "6", "9", "#"],
]
```

The script reads `raw.txt`, parses the `column` and `row` values, and reconstructs the flag:

```python
column, row, count = map(int, line.split(","))

character = keypad_map[column - 1][row - 3 - 1]
output += character * count
```

Running the script yields the flag.
