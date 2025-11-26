#!/usr/bin/env python3

import sys

alphabet = "abcdefghijklmnopqrstuvwxyz"


def shift_chars_back(text, pos):
    out = ""
    for letter in text:
        if letter in alphabet:
            letter_pos = (alphabet.find(letter) - pos) % 26
            out += alphabet[letter_pos]
        else:
            out += letter
    return out


def decrypt_text(text):
    counter = 0
    decrypted_text = ""

    for i in range(0, len(text), 10):
        counter = (counter + 1) % 26
        decrypted_text += shift_chars_back(text[i : i + 10], counter)
    return decrypted_text


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <filename>.encrypted")
        sys.exit(1)
    filename = sys.argv[1]

    with open(filename, "r") as f:
        encrypted_data = f.read()

    decrypted_data = decrypt_text(encrypted_data)

    output_filename = filename.replace(".encrypted", ".decrypted")
    with open(output_filename, "w") as f:
        f.write(decrypted_data)
