pragma solidity ^0.7.6;

contract Chal {
    address public owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    // Accept ether
    receive() external payable {}
    
    // Trade function
    function trade() external payable {
        uint256 amount = msg.value;
        require(amount >= 3 ether, "You must trade at least 3 ETH");
        uint256 balanceBeforeDeposit = address(this).balance - msg.value;
        uint256 fee = (amount - 3 ether) * (balanceBeforeDeposit / 1 ether) * 6 / 1000;
        uint256 maximumReturn = 150 ether;

        uint256 outputAmount = amount * 9 / 10 - fee;
        if (outputAmount > maximumReturn) {
            outputAmount = maximumReturn;
        }

        payable(msg.sender).transfer(outputAmount);
    }
    
    // Get balance
    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }
}