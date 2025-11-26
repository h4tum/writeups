# Writeup: Captcha 2.0 (WHY2025 CTF)

Event: [WHY2025 CTF](https://ctf.why2025.org/) ([CTFTime](https://ctftime.org/event/2680))
Challenge: Captcha 2.0
Category: Networking

We are provided with a PCAP file `captcha-2.0.pcap` capturing network traffic.

## Analysis

I opened the PCAP file in Wireshark. To analyze the web traffic more easily, I used the "Export Objects -> HTTP" feature in Wireshark to extract all HTTP responses transmitted during the session.

Upon inspecting the extracted files (named `home(000).php` through `home(109).php`), I identified a Boolean-based Blind SQL Injection attack against the `home.php` endpoint.

The server response indicates whether the injected SQL condition was true or false:

- True: The server reflects the injected payload in the "Welcome" message.
  Example from `home(000).php`: `Welcome user test' AND (SELECT SUBSTR(sql,1,1) FROM SQLITE_MASTER LIMIT 0,1) = 'C. Nothing much to do here...`

- False: The server returns a generic welcome message.
  Example from `home(003).php`: `Welcome user test. Nothing much to do here...`

## Solution

The attacker extracts the password from `userTable` using the pattern:
`... SELECT SUBSTR(password, N, 1) FROM userTable ...`

I iterated through the extracted files starting from `home(071).php`, picking the character reflected in the "Welcome" message only when the file contained the reflected SQL payload (indicating a match).

- `home(071).php`: matches `f`
- `home(072).php`: matches `l`
- `home(073).php`: matches `a`
- `home(074).php`: (False response, skipped)
- `home(075).php`: matches `g`
- ...

Combining these characters reveals the flag.
