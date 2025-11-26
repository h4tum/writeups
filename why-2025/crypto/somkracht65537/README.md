# Writeup: Somkracht 65537 (WHY2025 CTF)

**Event:** [WHY2025 CTF](https://ctf.why2025.org/) ([CTFTime](https://ctftime.org/event/2680))
**Challenge:** Somkracht 65537
**Category:** Cryptography
**Solved by:** [dopri](https://github.com/DoPri/)

We are provided with a Python script `challenge.py`.

## Initial Analysis

The `challenge.py` script generates a standard RSA modulus $N = p \cdot q$ and encrypts a flag/message twice using two different public exponents:

1.  $e_1 = 65537$ (Standard RSA exponent)
2.  $e_2 = p + q$

I was given $N$, $ct_1 = m^{e_1} \pmod N$, and $ct_2 = m^{e_2} \pmod N$. I did not know $p$ or $q$.

## Solution

This challenge relies on the mathematical relationship between the sum of primes ($p+q$) and Euler's totient function $\phi(N)$.

Recall that:
$$ \phi(N) = (p-1)(q-1) = pq - (p+q) + 1 = N - (p+q) + 1 $$

Rearranging this for $p+q$:
$$ p+q = N + 1 - \phi(N) $$

Now look at the second encryption:
$$ ct_2 \equiv m^{p+q} \pmod N $$
Substituting $(p+q)$:
$$ ct_2 \equiv m^{N + 1 - \phi(N)} \pmod N $$
$$ ct_2 \equiv m^{N+1} \cdot m^{-\phi(N)} \pmod N $$

By Euler's Theorem, $m^{\phi(N)} \equiv 1 \pmod N$, so $m^{-\phi(N)} \equiv 1 \pmod N$.
Therefore:
$$ ct_2 \equiv m^{N+1} \pmod N $$

I now effectively had the message encrypted with two _known_ exponents:

1.  $e_A = 65537$
2.  $e_B = N + 1$

Since $\gcd(e_A, e_B) = \gcd(65537, N+1)$ is very likely to be 1, I could perform a **Common Modulus Attack**.

Using the Extended Euclidean Algorithm, I found integers $a$ and $b$ such that:
$$ a \cdot e_A + b \cdot e_B = 1 $$

I could then recover the message $m$:
$$ m \equiv ct_1^a \cdot ct_2^b \pmod N $$

I wrote `exploit.py` to implement this attack and recover the flag.
