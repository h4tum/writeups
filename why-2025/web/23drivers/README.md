# Writeup: 23drivers (WHY2025 CTF)

- **Event:** [WHY2025 CTF](https://ctf.why2025.org/) ([CTFTime](https://ctftime.org/event/2680))
- **Challenge:** 23drivers
- **Category:** Web
- **Solved by:** [dopri](https://github.com/DoPri/)

We are provided with a web challenge located at `https://23drivers.ctf.zone/`. The website contained a form asking for a "secret code".

## Initial Analysis

The hints on the page suggested a code format starting with "23D". A check of the input mechanism or blind guessing led to the hypothesis that the code consisted of this prefix followed by a short alphanumeric suffix.

## Solution

I developed a Python script to brute-force the secret code. The script assumes the code structure is `23D` followed by 3 characters from the set `A-Z` and `0-9`. This results in a search space of $36^3 = 46,656$ combinations, which is manageable for an online brute-force attack.
