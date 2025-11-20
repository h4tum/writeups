
import solcx
import os

"""
Collection of helper functions/routines for blockchains, WIP
"""

ETHER = 10**18

def compile_contract(filename, contractname = None):
    if contractname is None:
        contractname = os.path.basename(filename).removesuffix(".sol")
    temp_file = solcx.compile_files(filename)
    tag = f'{filename}:{contractname}'
    return temp_file[tag]['abi'], temp_file[tag]['bin']


def construct_contract(w3, contract_blueprint, constructor_args, *args, **kwargs):
    tx_hash = contract_blueprint.constructor(*constructor_args).transact(*args, **kwargs)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contractAddr = tx_receipt["contractAddress"]
    return w3.eth.contract(address=contractAddr, abi=contract_blueprint.abi, bytecode=contract_blueprint.bytecode)


