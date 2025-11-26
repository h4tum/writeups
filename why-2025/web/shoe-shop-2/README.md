# Writeup: Shoe Shop 2 (WHY2025 CTF)

Event: [WHY2025 CTF](https://ctf.why2025.org/) ([CTFTime](https://ctftime.org/event/2680))
Challenge: Shoe Shop 2
Category: Web
Solved by: [dopri](https://github.com/DoPri/)

The target is the web shop at "shoe-shop-2.ctf.zone". I need to access the admin's cart to retrieve the flag.

## Initial Analysis

I started by browsing the website and inspecting the HTTP requests in my browser. I noticed the `username` cookie contained a Base64-encoded string.

From the previous Shoe Shop challenge, I already knew the underlying plaintext structure was `page=cart&id=72` (with 72 being my user ID).

I determined that the application uses a simple XOR stream cipher with a reused keystream. Since I had the ciphertext from the cookie and the known plaintext structure, I could trivially recover the keystream.

## Solution

I wrote the script `exploit.py` to solve the challenge.

I took the `username` cookie I observed and defined the known plaintext `page=cart&id=72`. I derived the keystream by XORing these two values.

With the keystream recovered, I could forge a valid payload for any user. I created a new payload targeting the admin's user ID 01:

I sent this forged payload to the server to access the admin's cart (user ID 01), where I found the flag in the item description.
