 # Thanks
 - Category: blockchain
 - Final point value: 100
 - Solved by: `fkil`

## Challenge Description

Tighten your seatbelts and get ready to embark on an exhilarating journey through the world of blockchain technology! This intro challenge will help you get started.

## Solution

This challenge is an intro to `blockchain`. In particular, the challenge contract has a `withdraw` function, which simply
allows us to withdraw all money. Therefore, we only need to perform the correct API calls to call this contract.

For this purpose, we use the `web3.py` framework and the python bindings for `solc-x`.

In particular, the process is the following:

 1. Start challenge and get all relevant parameters
 2. Create a `Web3` instance to communicate with the blockchain
 3. Compile the contracts with the `solcx` module to get ABI and bytecode so that we can call the contract
 4. Create respective `w3.eth.contract` objects to communicate with the contracts.
 5. Call `chal_instance.functions.withdraw(balance).transact()` to steal money

