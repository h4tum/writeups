#!/usr/bin/python

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
from private import flag, expected_aes_key

with open("/app/private_key.pem", "rb") as f:
        data = f.read()

private_key = RSA.import_key(data)
d = private_key.d
n = private_key.n

print("Authenticate yourself by sending the encrypted AES key:")
while True:
    try:
        c = int(input())
    except ValueError:
        print("Error: give me a number.")
        continue
    
    aes_key = pow(c, d, n)
    if aes_key >= 1 << 128:
        print("Error key is too large")
        continue

    if expected_aes_key != aes_key:
        print("Error wrong key")
        continue

    print("\nAuthentication succeeded here is the encrypted flag:")
    cipher = AES.new(long_to_bytes(aes_key), AES.MODE_GCM)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(flag)

    print((nonce + ciphertext + tag).hex())
    exit()