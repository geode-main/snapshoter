import json
from os import path
from web3 import Web3
from math import ceil
import utils.globals as globals
from utils.distribute import distWeighted
from utils.addresses import getAllUniqueAddresses
from utils.balances import getBalances

dir_path = path.dirname(path.realpath(__file__))
with open(f"{dir_path}/abi.json") as data_json:
    abi = json.load(data_json)


def _detect(address):
    cont = globals.w3.eth.contract(
        abi=abi, address=Web3.toChecksumAddress(address))
    try:
        sv = cont.functions.getShareValue().call()
        return sv > 0
    except:
        return False


def detect(address):
    if _detect(address):
        return True
    else:
        return False


def distribute(address, balance):
    # use getAllUniqueAddresses && getBalances to distribute balances and then return
    add = Web3.toChecksumAddress(address)
    everyone = getAllUniqueAddresses(token=add)
    creamLp = globals.w3.eth.contract(abi=abi, address=add)
    globals.currentToken = creamLp
    balances = getBalances(everyone)
    distributed = distWeighted(dict(zip(everyone, balances)), balance)
    print(f"distributed {ceil(balance/1e18)}")
    return distributed
