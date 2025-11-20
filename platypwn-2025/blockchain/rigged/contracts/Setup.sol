pragma solidity ^0.8.13;

import "./Chal.sol";

contract Setup {
    Chal public immutable TARGET;

    constructor() payable {
        // Create the challenge contract and pass the deployer (msg.sender) as the trusted backend
        TARGET = new Chal(msg.sender);
        
        // Require 100 ether to be sent during deployment
        require(msg.value == 100 ether, "Must send 100 ether");
        
        // Send all the ether to the challenge contract
        payable(address(TARGET)).transfer(100 ether);
    }

    function isSolved() public view returns (bool) {
        // Challenge is solved if the TARGET contract has less than 10 ether
        return address(TARGET).balance < 10 ether;
    }
}