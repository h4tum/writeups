pragma solidity ^0.8.13;

contract Chal {
    address public owner;
    address public casinoBackend;
    uint256 public constant MIN_BET = 0.05 ether;
    uint256 public constant MAX_BET = 1 ether;
    uint256 public nextBetId;

    struct Bet {
        address player;
        uint8 machine;
        uint8 games;
        uint256 amount;
        bool settled;
        bool won;
    }

    mapping(uint256 => Bet) public bets;
    mapping(address => uint8) public games;

    event BetPlaced(uint256 indexed id, address indexed player, uint256 amount);
    event BetResolved(uint256 indexed id, address indexed player, uint256 amount, bool won);

    // Accept a trusted backend address from the deployer (Setup)
    constructor(address backend) {
        owner = msg.sender;
        casinoBackend = backend;
        nextBetId = 1;
    }

    // Accept ether
    receive() external payable {}

    // Register a bet — RNG is handled off-chain by the casino RNG service.
    function playCoinFlip() external payable returns (uint256) {
        require(msg.value >= MIN_BET, "Must send ether to flip");
        require(msg.value <= MAX_BET, "Max 1 ether per flip");

        uint256 id = nextBetId++;
        games[msg.sender]++;
        uint8 machine = 1;
        bets[id] = Bet(msg.sender, machine, games[msg.sender], msg.value, false, false);

        emit BetPlaced(id, msg.sender, msg.value);
        return id;
    }

    function playBlackJack() external payable returns (uint256) {
        require(msg.value >= MIN_BET, "Must send ether to flip");
        require(msg.value <= MAX_BET, "Max 1 ether per flip");

        uint256 id = nextBetId++;
        games[msg.sender]++;
        uint8 machine = 2;
        bets[id] = Bet(msg.sender, machine, games[msg.sender], msg.value, false, false);

        emit BetPlaced(id, msg.sender, msg.value);
        return id;
    }

    function playRockPaperScissors() external payable returns (uint256) {
        require(msg.value >= MIN_BET, "Must send ether to flip");
        require(msg.value <= MAX_BET, "Max 1 ether per flip");

        uint256 id = nextBetId++;
        games[msg.sender]++;
        uint8 machine = 3;
        bets[id] = Bet(msg.sender, machine, games[msg.sender], msg.value, false, false);

        emit BetPlaced(id, msg.sender, msg.value);
        return id;
    }

    // Owner or trusted backend: settle a registered bet with outcome provided by off-chain RNG service.
    function settleCoinFlip(uint256 id, uint256 random_1_to_10) external {
        require(msg.sender == casinoBackend, "Only backend can settle");
        Bet storage b = bets[id];
        require(b.player != address(0), "Bet not found");
        require(!b.settled, "Already settled");

        bool outcome = (random_1_to_10 % 2) == 0;

        // effects first
        b.settled = true;
        b.won = outcome;

        if (outcome) {
            uint256 payout = b.amount * 2;
            // transfer after state update to mitigate reentrancy
            payable(b.player).transfer(payout);
        }

        emit BetResolved(id, b.player, b.amount, outcome);
    }

    function settleBlackJack(uint256 id, uint256 random_1_to_42) external {
        require(msg.sender == casinoBackend, "Only backend can settle");
        Bet storage b = bets[id];
        require(b.player != address(0), "Bet not found");
        require(!b.settled, "Already settled");

        bool outcome = false;
        uint256 payout = 0;

        if (random_1_to_42 == 21) {
            payout = (b.amount * 15) / 4; // 3.75x payout for blackjack
            outcome = true;
        }
        else if (random_1_to_42 < 21) {
            payout = b.amount;
            outcome = true;
        }
        else {
            outcome = false;
        }

        // effects first
        b.settled = true;
        b.won = outcome;

        if (outcome) {
            // transfer after state update to mitigate reentrancy
            payable(b.player).transfer(payout);
        }

        emit BetResolved(id, b.player, b.amount, outcome);
    }

    function settleRockPaperScissors(uint256 id, uint256 random_1_to_3) external {
        require(msg.sender == casinoBackend, "Only backend can settle");
        Bet storage b = bets[id];
        require(b.player != address(0), "Bet not found");
        require(!b.settled, "Already settled");

        bool outcome = false;
        uint256 payout = 0;

        if (random_1_to_3 == 1) {
            payout = b.amount * 2; // 2x payout for rock-paper-scissors
            outcome = true;
        }
        else if (random_1_to_3 == 2) {
            payout = b.amount;
            outcome = true;
        }
        else {
            outcome = false;
        }

        // effects first
        b.settled = true;
        b.won = outcome;

        if (outcome) {
            // transfer after state update to mitigate reentrancy
            payable(b.player).transfer(payout);
        }

        emit BetResolved(id, b.player, b.amount, outcome);
    }

    // Read a bet
    function getBet(uint256 id) external view returns (address player, uint8 machine, uint8 games, uint256 amount, bool settled, bool won) {
        Bet storage b = bets[id];
        return (b.player, b.machine, b.games, b.amount, b.settled, b.won);
    }

    // Get balance
    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }
}
