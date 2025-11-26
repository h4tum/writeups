# Writeup: IOT Breach (WHY2025 CTF)

- **Event:** [WHY2025 CTF](https://ctf.why2025.org/) ([CTFTime](https://ctftime.org/event/2680))
- **Challenge:** IOT Breach
- **Category:** Forensics
- **Solved by:** [dopri](https://github.com/DoPri/)

We are provided with the `IOT_breach.img` file which contains a Linux disk dump with an encrypted home folder.

## Analysis

Looking at the Apache logs, it is visible that an attacker used a bug to piece by piece write a file that encrypts the drive. I simulated this process in `script_from_log.sh`.

Examining `script_from_log.sh`, I found that the attacker created a Perl script named `enc.pl` by echoing base64 encoded content to a file and decoding it.

```bash
cat enc.b64 | base64 -d > enc.pl
# cd /files && perl enc.pl L0s3@llYourF1l3s
# wipe /files/*.jpg
# wipe /files/enc.*
```

The comments at the end of the script are crucial. They show the exact command including the password used to execute the encryption script:

```bash
perl enc.pl L0s3@llYourF1l3s
```

Decoding the `enc.b64` content (or reading the reconstructed `enc.pl`) confirmed it uses `Crypt::Mode::CBC` with AES and a hardcoded initialization vector (IV).

```perl
my $cipher = Crypt::Mode::CBC->new("AES");
# ...
my $encrypted = $cipher->encrypt($data, $password, "R4ND0MivR4ND0Miv");
```

The IV is `R4ND0MivR4ND0Miv`.

## Solution

To recover the files, I wrote a decryption script `decrypt.py` that uses AES-CBC with the recovered password and IV.

My `decrypt.py` script implements the decryption logic:

```python
IV = b"R4ND0MivR4ND0Miv"
PW = "L0s3@llYourF1l3s"
# ...
cipher = AES.new(key, AES.MODE_CBC, IV)
decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
```

After running the script, I recovered the encrypted pictures, one of which contained the flag.
