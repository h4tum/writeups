pragma solidity ^0.8.13;

import "./Chal.sol";

contract Setup {
    Chal public immutable TARGET;

    constructor() payable {
        TARGET = new Chal();

        require(msg.value == 100 ether, "Must send 100 ether");

        payable(address(TARGET)).transfer(100 ether);
    }

    function isSolved() public view returns (bool) {
        return address(TARGET).balance < 10 ether;
    }
}
