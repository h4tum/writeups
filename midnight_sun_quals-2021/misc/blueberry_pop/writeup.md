
## blueberry pop

Solved by: `fkil`

### Description

The challenge consists of an email with two attachments:
 - A zip containing secret information in an encrypted way (probably the flag)
 - The encryption app (an ELF file)

### Solution

After inspecting the encryption app, we found out that it is a Python program packed with PyInstaller. To extract the python files, we used PyInstaller Extractor(https://github.com/khiemdoan/pyinstaller_extractor).
However, we had to modify the source code of the extractor to ignore errors when it tried to unpack CPython components.

When inspecting the extracted `main.py` file, we make the following observations:
 - The encryption uses a generated ephemeral key to encrypt the contents in AES-CTR mode. The ephemeral key is then encrypted using a long-term shared key and put into the header of the encrypted file
 - The seed for the generation of the ephemeral key is not random

Therefore, our goal was to figure out the seed, and then generate the ephemeral key using the seed.

The code for the generation of the key is the following (note: get_rng is called with seed=None):
```python
def get_rng(seed=None):
    rnd = random.Random()
    if not seed:
        user = getpass.getuser()
        ts_ms = datetime.datetime.now().isoformat(sep='!', timespec='milliseconds')
        rdata = str(random.getrandbits(256))
        print(f"rdata = {rdata}")
        print(f"ts_ms = {ts_ms}")
        seed = f"{user}_{ts_ms}_{rdata}"
    rnd.seed(seed)
    return rnd


def generate_ephemeral_key() -> bytes:
    rnd = get_rng()
    return bytes((rnd.getrandbits(8) for _ in range(32)))
```

If we inspect the components of the seed, we can observe that we can accurately figure out most of them:
 - user: The user is likely the same as the sender of the e-mail: `erism`
 - ts_ms: The last modified date in the zip gives us a good estimate about the creation of the file
 - rdata: The main function of the program initializes the pseudorandom generator with a constant seed and, therefore, rdata is also constant. `random.seed('0427cb12119c11aff423b6333c4189175b22b3c377718053f71d5f37fd2a8f22')`

The only remaining part is to be careful about the timezone difference in the last-modified date and to brute-force the milliseconds component of the time. For this, we used the decryption routine in `main.py` and modified the `get_ephemeral_key` function to use the seed of the brute-force.
After a short amount of time, we were rewarded with the flag.
