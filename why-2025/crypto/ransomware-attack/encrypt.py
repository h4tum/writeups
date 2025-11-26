#!/usr/bin/env python3

# Ransomware encryptur
# The best encryptur on the planet, I wrote it myself

import sys

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def shift_chars(text, pos):
    out = ""
    for letter in text:
        if letter in alphabet:
            letter_pos = (alphabet.find(letter) + pos) % 26
            new_letter = alphabet[letter_pos]
            out += new_letter
        else:
            out += letter
    return out

def encrypt_text(text):
    counter = 0
    encrypted_text = ""

    for i in range(0, len(text), 10):
        counter = (counter + 1) % 26
        encrypted_text += shift_chars(text[i:i+10], counter)
    return encrypted_text

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <filename>")
        sys.exit(1)
    filename = sys.argv[1]

    with open(filename, "r") as f:
        data = f.read()

    encrypted_data = encrypt_text(data)

    with open(f"{filename}.encrypted", "w") as f:
        f.write(encrypted_data)
