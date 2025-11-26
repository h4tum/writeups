keypad_map = [
    ["1", "4", "7", "*"],
    ["2", "5", "8", "0"],
    ["3", "6", "9", "#"],
]


output = ""
with open("raw.txt", "r") as file:
    for line in file:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        column, row, count = map(int, line.split(","))
        character = keypad_map[column - 1][row - 3 - 1]

        output += character * count
print(f"flag{{{output}}}")
