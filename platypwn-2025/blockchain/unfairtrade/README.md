
# Unfair Trade
 - Category: blockchain
 - Final point value: 100
 - Solved by: `fkil`

## Challenge Description

You found this smart contract deployed on the Ethereum blockchain. It looks unfair, or does it?

## Solution

The challenge contract has a function `trade`, which we can send money to and will give us back parts of the money. The formula for the fee is very suspicious. Furthermore, the `outputAmount` is an unsigned integer, and, thus, if the fee would ever be more than `msg.value * 9 / 10`, the `outputAmount` would become a very large number.

Additionally, there is a check that if the amount would be more than 150, it will only send 150 back. This is also helpful in that case: if the outputAmount wraps around, the number will be in the order of $2^{255}$, but the contract would definitely not have that much money and the request would fail. By capping the amount to 150, we can actually retrieve money. Furthermore, the `isSolved()` function for this task doesn't require us to completely deplete the contract, but make the contract have less than 50 ether. Thus, by triggering this scenario once, we solve the task.

The actual formula for the outputAmount is the following (in ether):

$$(amount * 9 / 10) - (amount - 3) * (balanceBeforeDesposit) * 6 / 1000$$

Both us and the challenge contract start off with 100 ether, thus the maximum $balanceBeforeDeposit$ is $(200 - amount)$. Since the transaction will also require some *gas*, we actually do not want to use 200, but slightly less.

By inserting that condition, the formula would be:

$$(amount * 9 / 10) - (amount - 3) * (200 - amount - \epsilon) * 6 / 1000$$

This ends up being a quadratic function, which can be optimized to find a value lower than 0. However, before we try fancy stuff, we could just try evaluating this function for possible amounts in the interval $(3;100)$ and see if any value is negative. We initially took $\epsilon$ as 4 and then printed all values the following way:

```python
print([amount for amount in range(100) if (amount * 9 / 10) - ((amount - 3) * (196-amount) * 6 / 1000) < 0])
```

The result is `[22, 23, 24, 25, 26, 27]`, thus if we send that much money and make the other site have $196-amount$ ether, we get 150 ether back and solve the challenge.

The solution script then performs the following steps:
 - Choose `24` as the amount we want to send at the end
 - Feed the contract money until it has more than `196-24=172` ether
 - Send `24` ether and win.

