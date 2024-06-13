# Boombox
 - Category: crypto
 - Final point value: 126
 - Number of solves: 47
 - Solved by: `fkil`

### Challenge Description

I have no clue of rust and no clue of crypto, but then with no challenge I stood crying in the rain and rusted.

### Solution

The challenge implements the [Merkle–Hellman knapsack cryptosystem](https://en.wikipedia.org/wiki/Merkle%E2%80%93Hellman_knapsack_cryptosystem) with a block size of $n=42$. We noticed the low block size and decided to brute-force the corrept input. Specifically, we know that the input characters are ASCII printable and thus each block has $<38$ bits entropy.

As 42 bits is not divisible by 8, each block has partial bits of a character at the end or beginning or both. As such, for each block we created three bitsets, one for the beginning, one for the middle characters and one for the end.

Brute-forcing could be easily parallelized in Rust via `par_iter()` from the `rayon` crate. On an i5-13600K it took roughly 1.5 hours to get the flag.

