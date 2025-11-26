import itertools
import re


def decrypt_vba_text(encrypted_text: str, username: str) -> str:
    key = username.lower().replace(" ", "")

    if not key:
        raise ValueError("Username cannot be empty or only spaces, as it results in an empty key.")

    decrypted_chars = []

    for i, char in enumerate(encrypted_text):
        key_char = key[(i + 1) % len(key)]
        decrypted_char_code = ord(char) ^ ord(key_char) ^ 0x7B

        decrypted_chars.append(chr(decrypted_char_code))

    return "".join(decrypted_chars)


if __name__ == "__main__":
    # encrypted_content = u"""Swywy}wcm3U`}a{l2Hlpf`rmA{nfu{>Yi}}j{ev%#:2Iaqgdy~qdf-Sll25Zrlizu`b}q%>[P3.<#/q~luaj*-:"#j!rs4v,k| <u-9'$wity8$9!.qX~ddsh>Gm}idu`"""
    encrypted_content = """q~luaj*-:"#j!rs4v,k| <u-9'$wity8$9!.q"""
    print(decrypt_vba_text(encrypted_content, "Olivia Renshaw".replace(" ", "").lower()))
