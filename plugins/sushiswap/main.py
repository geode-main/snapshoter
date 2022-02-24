
import json
from os import path
from math import ceil
from web3 import Web3
from dotenv import load_dotenv
import utils.globals as globals
from utils.addresses import getAllUniqueAddresses
from utils.balances import getBalances
from utils.distribute import distWeighted

dir_path = path.dirname(path.realpath(__file__))
with open(f"{dir_path}/abi.json") as data_json:
    abi = json.load(data_json)


def _detect(address):
    try:
        cont = globals.w3.eth.contract(
            abi=abi, address=Web3.toChecksumAddress(address))
        fac = cont.functions.factory().call()
        return Web3.toChecksumAddress(fac) == "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac"
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
    sushiLp = globals.w3.eth.contract(abi=abi, address=add)
    globals.currentToken = sushiLp
    balances = getBalances(everyone)
    distributed = distWeighted(dict(zip(everyone, balances)), balance)
    print(
        f"distributed {ceil(balance/1e18)}")
    return distributed
