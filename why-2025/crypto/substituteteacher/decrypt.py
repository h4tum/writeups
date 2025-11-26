plain = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
cipher = "kehmywrgupjtczqaxfnlvsodbiKEHMYWRGUPJTCZQAXFNLVSODBI"

assert len(plain) == len(cipher)

decrypt_map = {plain[i]: cipher[i] for i in range(len(plain))}


def mono_decrypt(text: str):
    return "".join(decrypt_map[ch] if ch in plain else ch for ch in text)


with open("story.txt", "r") as f:
    cipthertext = f.read()


plaintext = mono_decrypt(cipthertext)
print(plaintext)
