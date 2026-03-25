# Smooth RSA
Category: `crypto`

## Setup

We are given the following files:

`server.py`:
```Python
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
```

`c.txt`:
```
3227373577593336048379530132111996583661354653402137933092594205391382591402500219159973862322197530568103063335806544079801231023777202299487714452208845334519081976597654707186657255119828064693752845924613678901879054543973094882714434289505682182444816314553062129564845032182306297438918744603313192476971585056640249177597359551408167051225327644050877266385402096106483995535650864066614518436189669134524607166065573631001172422642630957369559313710724816293754995818675884768815441629421482677778375223538332501843494874432491605398973373895471689655016275691146766921786113039348617885174558548211659846726
```

`public_key.pem`:
```
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3YYKS/BRY9GIwDvA9AOI
YxGRWvC3kU3h+xmxt2H/XvSw/5IDgMlHmL5nMcgvaY0Sw+5V6HFwlua3BTPmeSXD
KzatwG2126l/oSOnV40p5RV4rVeQd9sOJntbkb51Fz+kp2UG/Yyp+bl+KkE62xDB
glbuwL20kgY4OGUeVkHgLhqe2Sj/FX2y8Fzl+xy8Layg9pLOh22QJoUzHo3wlRp7
DenXrudPO7ObmALDDNnbhqi394fBg0vkNPrTg5pwgxofCbcpC8/hXmeMU4QOJdDl
CO05eKdo7+vjybCzXJ/PjqEtK8mSvdIS5LpHR+J7dq5Uy9UEwG2Vw6wThHTVWHDM
GwIDAQAB
-----END PUBLIC KEY-----
```

$N = p \cdot q = 27964763094083956636811035489361773889660725417245907604567835243741299648611476459152698777714050435058738635038903990791382178059740273584085687297899387374227828386793167145037203964445257515330466558987147074808790266155344060157935319045016081124639205361494086095121967096176263771035268581756016652461590975580194951499676046394386815216993126391446616723066838308775402203738126446881805918807124816714564951606683279847279704355299377008024589904171096997045530657685923998659542332846553502348350591779292608546124483550272820105484669373734406418933504416482962713040374725650128583746470208787702376090651$
$e = 65537$

In the code we can see, that the server decrypts a given $c$ for us, using the RSA private key. 
Afterward it checks that the resulting message is smaller than $2^{128}$ because it should be an AES-128 key. If the condition fails, an error is reported. 
If the key does not match the expected AES key, it returns a different error.
Lastly, the flag is encrypted with AES GCM using the computed AES key and a (securely) random nonce. 

For testing, I also created a [Dockerfile](./Dockerfile) and [private.py](./private.py) for testing purposes. Note that the private/public key pair is different in the container.

## RSA basics

Those are the basic operations needed for RSA.

$p, q$: two large Primes chosen at random.
$N = p \cdot q$: the RSA modulus; part of the public and private key
$e$: part of the public key; most often $e = 65537$
$\varphi$ is the Euler Phi Function that computes the number of natural numbers $k$ lower than $N$ that are co-prime to $n$, i.e. $\gcd(k, N) == 1$
$\varphi(N) = \varphi(p \cdot q) = (p - 1) \cdot (q - 1)$
$d \equiv e^-1 ~(\text{mod}~ \varphi(N))$: part of the private key
i.e.: $e \cdot d \equiv 1~(\text{mod}~ \varphi(N))$

encryption: $c \equiv m^e~(\text{mod}~ N)$
encryption: $m \equiv c^d~(\text{mod}~ N)$


## Attack Vector

The attackable part of the code, is the way the errors are handled: This is effectively a padding oracle. This is also known as the Bleichenbacher Attack or as Adaptive chosen-ciphertext attack.

This allows us to supply the server with messages of the following form:
$c' \equiv c \cdot s^e ~(\text{mod}~ N)$

When the server decrypts $c'$, the resulting message is:
$m' \equiv c'^{~d} \equiv (c \cdot s^e)^{~d} \equiv c^d \cdot s^{e^d} \equiv m \cdot s^1 \equiv m \cdot s ~(\text{mod}~ N) $

As the AES key $m$ is a valid AES-128 key, it is smaller than $2^{128}$. By selecting specific values for $s$ we can use the oracle to leak information about $m$, specifically whether $m \cdot s \geq 2^{128}$.

## Method I: Bounding $m$

As first idea, we would like to find $s'$ such that $m \cdot s' < 2^{128} \leq m \cdot (s'+1)$. By iteratively using higher $s'$, starting at $2$ we can find that tipping point.

```Python
for s in range(2, 1000):
    c_ = (c * pow(s, e, N)) % N
    if oracle(c_):
        break
```

Alternatively, we can raise the upper bound exponentially and then combine it with binary search to reduce the number of required network requests (which was very relevant as the network was severely overloaded):

```Python
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
    
```

Afterward, we can get an estimate for $m$ by manipulating the previous equation:
$m \cdot s' < 2^{128} \Leftrightarrow m < \lfloor\frac{2^{128}}{s'}\rfloor$
$m \cdot (s' + 1) \geq 2^{128} \Leftrightarrow m \geq \lceil\frac{2^{128}}{s' + 1}\rceil$

For the challenge setup, we get $s = 14$. 
This results in the following bounds:
$$m \in [ 22685491128062563916067208304141533184, 24305883351495603183850619710941954048]$$

This is still waaaay too large to brute force in a CTF.

## Method II: Extracting small Prime factors of $m$

It would be helpful to specify $s = 0.5$ (or any other fraction) in order to test for divisibility. In fact, we can do that, because we can calculate the modular inverse $s_{inv} = s^-1 ~(\text{mod}~ N)$.

We can always do this for reasonably small $s$ because 
- $N = p \cdot q$, 
- $s \leq p$
- $s \leq q$
- thus $gcd(s, N) = 1$

if $s | m$ ($s$ divides $m$) then $m \cdot s^{-1} < m ~(\text{mod}~N)$ else $m \cdot s^{-1} > m ~(\text{mod}~N)$

Thus we can factorize $m$, up to a reasonably small bound to keep computational efforts low. I chose to try every $\text{prime} < 10000$. This got us the following prime factors: 

$$2,17,23,41,71,307,461,883,971$$


```Python
factors = []
for prime in primes:
    c_ = (c * pow(prime, -e, N)) % N
    if not oracle(c_):
        factors.append(prime)
```

This attack would fail if the AES key would only have large prime factors, which in general is unlikely for a randomly chosen AES key.

## Extracting the full AES key

Now we can use Method I with $c' \equiv c \cdot \left(\prod\limits_{p \in primes} p^{-1}\right)^e ~(\text{mod~} N)$, to find a tipping point such that we have a range of $23$ possible values for $m$. The range will be much smaller as $m' << m$ and thus $s'$ much larger is.

We can retrieve the encrypted flag from the server by sending the correct $c$ and then bruteforce decrypt with all of the 23 potential keys.

## Solve Script

```Python
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
```