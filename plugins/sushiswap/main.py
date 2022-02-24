
import json
from os import path
from math import ceil
from web3 import Web3
from multiprocessing import Pool
import utils.globals as globals
from utils.addresses import getAllUniqueAddresses
from utils.balances import getBalances
from utils.distribute import distWeighted, addWeighted

dir_path = path.dirname(path.realpath(__file__))
with open(f"{dir_path}/abi.json") as data_json:
    abi = json.load(data_json)

with open(f"{dir_path}/masterChef.json") as data_json:
    masterABI = json.load(data_json)

masterAddress = Web3.toChecksumAddress(
    "0xEF0881eC094552b2e128Cf945EF17a6752B4Ec5d")


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


def getAddressMasBal(address):
    print(address, end="\r", flush=True)
    bal = None
    counter = 0
    while bal is None:
        try:
            bal = globals.masterchef.functions.userInfo(
                7, address).call(block_identifier=globals.snapshot)
            bal = bal[0]
        except:
            if counter < 10:
                counter += 1
            else:
                raise Exception("couldn't get the data...")
    return bal


def getMasterBalances(addresses):
    print("\nReading masterchef balances")
    with Pool() as pool:
        BALANCES = pool.starmap(getAddressMasBal, zip(list(addresses)))
    return BALANCES


def distribute(address, balance):
    # use getAllUniqueAddresses && getBalances to distribute balances and then return
    add = Web3.toChecksumAddress(address)
    sushiLp = globals.w3.eth.contract(abi=abi, address=add)
    globals.currentToken = sushiLp
    people = getAllUniqueAddresses(token=add)
    balances = getBalances(people)

    # distribute Sushiswap masterchef too if token is ruler
    if globals.mainToken.address == Web3.toChecksumAddress("0x2aeccb42482cc64e087b6d2e5da39f5a7a7001f8"):
        globals.masterchef = globals.w3.eth.contract(
            abi=masterABI, address=masterAddress)
        masterBalance = dict(zip(people, balances))[masterAddress]
        print(f"Masterchef balance:{masterBalance}")
        masBalances = getMasterBalances(people)
        masSup = sum(masBalances)
        if not masSup == masterBalance:
            raise Exception(
                "Total Supply and Balances doesn't match: MasterChef")

        balances = addWeighted(
            dict(zip(people, balances)),  dict(zip(people, masBalances)), masterBalance)

        balances[masterAddress] == 0
        print(f"Masterchef balance:{balances[masterAddress]}: distributed")
        distributed = distWeighted(balances, balance)
    else:
        distributed = distWeighted(dict(zip(people, balances)), balance)

    print(
        f"distributed {ceil(balance/1e18)}")
    globals.currentToken = globals.mainToken
    return distributed
