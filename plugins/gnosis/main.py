import utils.globals as globals
import json
from os import path
from web3 import Web3

dir_path = path.dirname(path.realpath(__file__))
with open(f"{dir_path}/abi.json") as data_json:
    abi = json.load(data_json)


def _detect(address):
    try:
        cont = globals.w3.eth.contract(
            abi=abi, address=Web3.toChecksumAddress(address))
        name = cont.functions.NAME().call()
        return name == "Gnosis Safe"
    except:
        return False


def detect(address):
    if _detect(address):
        return True
    else:
        return False
