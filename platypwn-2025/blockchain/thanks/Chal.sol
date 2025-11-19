pragma solidity ^0.8.13;

contract Chal {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    receive() external payable {}

    function withdraw(uint256 amount) external {
        // require(msg.sender == owner, "Not owner");
        payable(msg.sender).transfer(amount);
    }

    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }
}
