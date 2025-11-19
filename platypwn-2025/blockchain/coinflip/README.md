 # Coin Flip
 - Category: blockchain
 - Final point value: 100
 - Solved by: `fkil`

## Challenge Description

Maybe you can win, but you need to get really lucky...

## Solution

The challenge contract has a `flip()` function, which pays out money in case the least significant bit
of the last block was 0. Since this is not true random, and we can determine the outcome beforehand, we
can easily steal all money.

Our approach will be the following:

 1. Compute the outcome.
 2. If the outcome lets us win, bet the maximum possible ether, otherwise bet the minimum possible ether.
 3. Repeat 2 until we stole all money.

To get the last block, we can use the following snippet of `web3.py`:

```python
bnum = w3.eth.block_number
block = w3.eth.get_block(bnum)
bhash = int.from_bytes(block.hash, byteorder="big")
```
