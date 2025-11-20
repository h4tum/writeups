pragma solidity ^0.7.6;

import "./Chal.sol";

contract Setup {
    Chal public TARGET;

    constructor() payable {
        // Create the challenge contract
        TARGET = new Chal();
        
        // Require 100 ether to be sent during deployment
        require(msg.value == 100 ether, "Must send 100 ether");
        
        // Send all the ether to the challenge contract
        payable(address(TARGET)).transfer(100 ether);
    }

    function isSolved() public view returns (bool) {
        // Challenge is solved if the TARGET contract has less than 50 ether
        return address(TARGET).balance < 50 ether;
    }
}