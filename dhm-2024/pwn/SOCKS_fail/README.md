SOCKS fail
===

- Category: pwn
- Final point value: 403
- Number of solves: 5
- Solved by: fkil

## Challenge Description

Hosting a SOCK5 server can be scary. Go exploit it!

## Overview

The vulnerable program implements a vulnerable SOCK5 server via a fork-server architecture. We have a stack buffer-overflow and can abuse the fork-server architecture to exploit it without direct leaks. Furthermore, we are given a `win` function that will start a listener to give direct shell access.

## Exploiting fork servers in general

Stack overflows on fork server architectures are generally easier exploit. This is due to the fact that no further randomization occurs after `fork` and the ASLR and canary values will be the same for every instance. Given an oracle whether the program crashed or not, bytes can be brute-forced one-by-one.

To elaborate this point: We can guess a canary value and overflow the canary accordingly. If we guessed right, the function will return normally, but if we guessed wrong, the program will crash. We can use the same logic for all types of pointers such as the return value. In fact, this would even allow exploiting the program without [having any binary or source code](https://ieeexplore.ieee.org/abstract/document/6956567).

## The vulnerability

The server has a vulnerability in the `talk` routine for negotiating where the SOCK5 server should forward a connection to. The client sends a 1-byte value `nmethods`, which will be used by the server as argument to `recv`. However, the buffer is only `127` bytes big, while the max value of a byte is `255`. Thus, we have an overflow of `128` bytes.

## Exploitation

We use the aforementioned oracle technique to leak the stack canary, rbp, and return value. Specifically to get an oracle, we let the SOCK5 server connect back to itself via `localhost:1024` and send initial handshake data to make the server respond.

If the `talk` function crashed, we will not receive any response, but if it did not crash we will receive a second handshake response (containing the chosen method).

Given the canary, rbp and return value, we can compute the address of the `win` function and overwrite the return value to it.
