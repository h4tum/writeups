#!/usr/bin/env python3
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes

from pwn import *

HOST = "smoothrsa.insomnihack.ch"
PORT = 971

with open("public_key.pem","r") as f:
    key = RSA.import_key(f.read())
    n = int(key.n)
    e = int(key.e)
with open("c.txt", "r") as c_f:
    c = int(c_f.read())

with open("primes.txt", "r") as primes_f:
    primes = list(map(int, primes_f.read().splitlines()))

B = 2**128

io = remote(HOST, PORT)
io.recvuntil(b"Authenticate yourself by sending the encrypted AES key:\n")

def query_integer(x):
    io.sendline(str(x).encode())
    resp = io.recvuntil(b"\n")
    if resp == b"\n":
        resp = io.recvuntil(b"\n")
    return resp

def oracle_test_cipher(c_int):
    resp = query_integer(c_int)
    if b"Error key is too large" in resp:
        return "TOO_LARGE"
    if b"Error wrong key" in resp:
        return "WRONG_KEY"
    if b"Authentication succeeded" in resp or b"here is the encrypted flag" in resp or b"encrypted flag" in resp:
        return resp
    return resp

def do_oracle(s: int):
    c_ = (c * pow(s, e, n)) % n
    return oracle_test_cipher(c_) == "TOO_LARGE"

def recover_aes_key():
    factors = {}
    m_small_factors = 1
    m_inv = 1
    idx = 0
    count = 0
    while idx < len(primes):
        a = primes[idx]
        if m_small_factors * a >= 2**128:
            break
        a_inv = pow(a, -1, n)
        if not do_oracle((m_inv * a_inv) % n):
            # this is a factor
            m_small_factors *= a
            m_inv = (m_inv * a_inv) % n
            count += 1
            print(f"Found factor: {a}")
        else:
            if count > 0:
                factors[a] = count
            count = 0
            idx += 1

    s_low = 1
    s_high = 2
    
    while not do_oracle((s_high * m_inv) % n):
        s_low = s_high
        s_high *= 2

    while s_high - s_low > 1:
        s_mid = (s_low + s_high) // 2
        if do_oracle((s_mid * m_inv) % n):
            s_high = s_mid
        else:
            s_low = s_mid
    
    print(f"s_low = {s_low}, s_high = {s_high}")
        
    rest_lower = B // s_high
    rest_higher = B // s_low
    print(f"m in [{rest_lower}, {rest_higher}], number of options = {rest_higher - rest_lower}")

    return [(m_small_factors * rest_pot) for rest_pot in range(rest_lower, rest_higher + 1)]


def get_encrypted_flag() -> bytes:
    resp = query_integer(c)
    assert resp == b'Authentication succeeded here is the encrypted flag:\n'
    return bytes.fromhex(io.recvuntil(b"\n", drop=True).decode())

def extract_cipher_hex(resp_text):
    # try to find hex blob in response
    import re
    m = re.search(r"([0-9a-fA-F]{2,})".encode(), resp_text)
    if not m:
        return None
    hexs = m.group(1)
    # choose the longest hex sequence
    candidates = re.findall(r"([0-9a-fA-F]{2,})", resp_text)
    hexs = max(candidates, key=len)
    return hexs

def decrypt_flag_from_hex(data: bytes, aes_key):
    key = long_to_bytes(aes_key)
    nonce = data[:16]
    tag = data[-16:]
    ciphertext = data[16:-16]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    plain = cipher.decrypt_and_verify(ciphertext, tag)
    return plain

aes_key_opts = recover_aes_key()
enc_flag = get_encrypted_flag()
for aes_key in aes_key_opts:
    try:
        flag = decrypt_flag_from_hex(enc_flag, aes_key)
        print("Flag (decrypted):")
        print(flag.decode(errors='ignore'))
        exit()
    except Exception:
        pass
print("Could not recover flag :(")
