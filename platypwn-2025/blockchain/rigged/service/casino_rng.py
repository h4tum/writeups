import os
import sys
import time
import argparse
import logging
import secrets

from web3 import Web3
from eth_account import Account

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

HTTP_PORT = os.getenv("HTTP_PORT", "8545")

# Minimal ABI for interacting with Chal: BetPlaced event and settleBet function
ABI = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "uint256", "name": "id", "type": "uint256"},
            {"indexed": True, "internalType": "address", "name": "player", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "BetPlaced",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "uint256", "name": "id", "type": "uint256"},
            {"indexed": True, "internalType": "address", "name": "player", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"},
            {"indexed": False, "internalType": "bool", "name": "won", "type": "bool"},
        ],
        "name": "BetResolved",
        "type": "event",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "id", "type": "uint256"},
            {"internalType": "uint256", "name": "outcome", "type": "uint256"},
        ],
        "name": "settleCoinFlip",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "id", "type": "uint256"},
            {"internalType": "uint256", "name": "outcome", "type": "uint256"},
        ],
        "name": "settleBlackJack",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "id", "type": "uint256"},
            {"internalType": "uint256", "name": "outcome", "type": "uint256"},
        ],
        "name": "settleRockPaperScissors",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    # add access to nextBetId and getBet so the service can scan for unsolved bets
    {
        "inputs": [],
        "name": "nextBetId",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "id", "type": "uint256"}],
        "name": "getBet",
        "outputs": [
            {"internalType": "address", "name": "player", "type": "address"},
            {"internalType": "uint8", "name": "machine", "type": "uint8"},
            {"internalType": "uint8", "name": "games", "type": "uint8"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
            {"internalType": "bool", "name": "settled", "type": "bool"},
            {"internalType": "bool", "name": "won", "type": "bool"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
]

# Minimal ABI for probing Setup: exposes TARGET() -> address
SETUP_ABI = [
    {
        "inputs": [],
        "name": "TARGET",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    }
]


def secure_randint(a: int, b: int) -> int:
    """Return a cryptographically secure random integer N such that a <= N <= b.

    Implemented using secrets.randbelow which returns [0, n).
    """
    if b < a:
        raise ValueError("secure_randint() upper bound must be >= lower bound")
    # secrets.randbelow(n) returns 0..n-1, so add a
    return secrets.randbelow(b - a + 1) + a


def main():
    parser = argparse.ArgumentParser(description="Casino RNG service: scans for unsolved bets and calls settleBet. Provide setup contract address.")
    parser.add_argument("uuid", help="Unique run id (for logging)")
    parser.add_argument("deployer_privkey", help="Deployer private key (hex, with or without 0x)")
    parser.add_argument("setup_contract", help="Setup contract address (positional) - used to read TARGET() which is the Chal address")
    args = parser.parse_args()

    priv = args.deployer_privkey
    if priv.startswith("0x"):
        priv = priv[2:]

    acct = Account.from_key(bytes.fromhex(priv))
    rpc_url = f"http://127.0.0.1:{HTTP_PORT}/{args.uuid}"
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.isConnected():
        logging.error("Unable to connect to RPC %s", rpc_url)
        sys.exit(1)

    # normalize and read setup -> TARGET
    def normalize_address(addr: str) -> str:
        if not addr:
            raise ValueError("empty address")
        addr = addr.strip()
        if not addr.startswith("0x"):
            addr = "0x" + addr
        if len(addr) != 42:
            raise ValueError("invalid length")
        try:
            return Web3.toChecksumAddress(addr)
        except Exception:
            return Web3.toChecksumAddress(addr.lower())

    try:
        setup_addr = normalize_address(args.setup_contract)
    except Exception as e:
        logging.error("Invalid setup_contract address %s: %s", args.setup_contract, e)
        sys.exit(1)

    setup_contract = w3.eth.contract(address=setup_addr, abi=SETUP_ABI)
    try:
        chal_addr_raw = setup_contract.functions.TARGET().call()
        chal_addr = Web3.toChecksumAddress(chal_addr_raw)
    except Exception as e:
        logging.exception("Failed to read TARGET() from Setup contract %s", setup_addr)
        sys.exit(1)

    contract = w3.eth.contract(address=chal_addr, abi=ABI)

    logging.info("Service %s running. Owner address: %s. Watching Chal contract: %s (setup: %s)", args.uuid, acct.address, chal_addr, setup_addr)

    # scanning loop: periodically query nextBetId and inspect each bet for unsettled state
    scan_interval = 1
    while True:
        try:
            total = contract.functions.nextBetId().call()
            if total and total > 1:
                # iterate all placed bets (1 .. nextBetId-1)
                for bid in range(1, int(total)):
                    try:
                        player, machine, games, amount, settled, won = contract.functions.getBet(bid).call()
                    except Exception as e:
                        logging.debug("Failed to read bet %s: %s", bid, e)
                        continue

                    # skip empty / non-existent
                    if player == "0x0000000000000000000000000000000000000000":
                        continue

                    if not settled:
                        if machine == 1:
                            # resolve it
                            if games > 3:
                                if secure_randint(1, 100) <= 40:
                                    r = secure_randint(1, 10)
                                else:
                                    r = secure_randint(1, 5) * 2 - 1
                            else:
                                r = secure_randint(1, 5) * 2
                            logging.info("Resolving bet %s (player=%s amount=%s wei) => outcome=%s", bid, player, amount, r)

                            tx_func = contract.functions.settleCoinFlip(bid, r)
                            nonce = w3.eth.getTransactionCount(acct.address)
                            try:
                                gas_est = tx_func.estimateGas({"from": acct.address})
                            except Exception:
                                gas_est = 200_000
                            tx = tx_func.buildTransaction(
                                {
                                    "from": acct.address,
                                    "nonce": nonce,
                                    "gas": int(gas_est * 1.2),
                                    "gasPrice": w3.eth.gas_price,
                                    "chainId": w3.eth.chain_id,
                                }
                            )

                            signed = acct.signTransaction(tx)
                            tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
                            logging.info("Submitted settle tx %s for bet %s", tx_hash.hex(), bid)
                            try:
                                receipt = w3.eth.waitForTransactionReceipt(tx_hash, timeout=30)
                                logging.info("Tx mined: %s status=%s", tx_hash.hex(), receipt.status)
                            except Exception as e:
                                logging.warning("Waiting for receipt failed: %s", e)

                        elif machine == 2:
                            # resolve it
                            if games > 3:
                                if secure_randint(1, 100) <= 30:
                                    r = secure_randint(1, 42)
                                else:
                                    r = secure_randint(22, 42)
                            else:
                                if secure_randint(1, 100) <= 50:
                                    r = secure_randint(1, 21)
                                else:
                                    r = 21
                            logging.info("Resolving bet %s (player=%s amount=%s wei) => outcome=%s", bid, player, amount, r)

                            tx_func = contract.functions.settleBlackJack(bid, r)
                            nonce = w3.eth.getTransactionCount(acct.address)
                            try:
                                gas_est = tx_func.estimateGas({"from": acct.address})
                            except Exception:
                                gas_est = 200_000
                            tx = tx_func.buildTransaction(
                                {
                                    "from": acct.address,
                                    "nonce": nonce,
                                    "gas": int(gas_est * 1.2),
                                    "gasPrice": w3.eth.gas_price,
                                    "chainId": w3.eth.chain_id,
                                }
                            )

                            signed = acct.signTransaction(tx)
                            tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
                            logging.info("Submitted settle tx %s for bet %s", tx_hash.hex(), bid)
                            try:
                                receipt = w3.eth.waitForTransactionReceipt(tx_hash, timeout=30)
                                logging.info("Tx mined: %s status=%s", tx_hash.hex(), receipt.status)
                            except Exception as e:
                                logging.warning("Waiting for receipt failed: %s", e)

                        elif machine == 3:
                            # resolve it
                            if games > 3:
                                if secure_randint(1, 100) <= 50:
                                    r = secure_randint(2, 3)
                                else:
                                    r = secure_randint(1, 3)
                            else:
                                if secure_randint(1, 100) <= 50:
                                    r = secure_randint(1, 3)
                                else:
                                    r = 1
                            logging.info("Resolving bet %s (player=%s amount=%s wei) => outcome=%s", bid, player, amount, r)

                            tx_func = contract.functions.settleRockPaperScissors(bid, r)
                            nonce = w3.eth.getTransactionCount(acct.address)
                            try:
                                gas_est = tx_func.estimateGas({"from": acct.address})
                            except Exception:
                                gas_est = 200_000
                            tx = tx_func.buildTransaction(
                                {
                                    "from": acct.address,
                                    "nonce": nonce,
                                    "gas": int(gas_est * 1.2),
                                    "gasPrice": w3.eth.gas_price,
                                    "chainId": w3.eth.chain_id,
                                }
                            )

                            signed = acct.signTransaction(tx)
                            tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
                            logging.info("Submitted settle tx %s for bet %s", tx_hash.hex(), bid)
                            try:
                                receipt = w3.eth.waitForTransactionReceipt(tx_hash, timeout=30)
                                logging.info("Tx mined: %s status=%s", tx_hash.hex(), receipt.status)
                            except Exception as e:
                                logging.warning("Waiting for receipt failed: %s", e)

            time.sleep(scan_interval)
        except KeyboardInterrupt:
            logging.info("Shutting down (keyboard interrupt)")
            break
        except Exception:
            logging.exception("Unhandled error while scanning; will retry after short sleep")
            time.sleep(3)


if __name__ == "__main__":
    main()