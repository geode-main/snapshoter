from math import ceil
from time import time
from web3 import Web3
import utils.globals as globals
from utils.data import collectTokensData, saveResults
from utils.addresses import getAllUniqueAddresses
from utils.balances import getBalances
from utils.contracts import distributeContractBals
from utils.blacklist import applyBlack

tokens = None


def snapshot(token):
    print(f"\n{token.capitalize()}:")
    start_time = time()
    balancesOfEveryone = {}
    balancesOfEveryone[token] = {}

    globals.creation = tokens[token]["creation"]
    globals.snapshot = tokens[token]["snapshot"]
    globals.currentToken = globals.mainToken = globals.w3.eth.contract(
        abi=tokens[token]["abi"], address=Web3.toChecksumAddress(tokens[token]["address"]))

    totSup = globals.mainToken.functions.totalSupply().call(
        block_identifier=globals.snapshot)

    everyone = getAllUniqueAddresses(
        token=Web3.toChecksumAddress(tokens[token]["address"]), )

    balances = getBalances(everyone)
    sumSup = sum(balances)

    if not sumSup == totSup:
        raise Exception("Total Supply and Balances doesn't match")
    if len(everyone) != len(balances):
        raise Exception("address and balances length doesn't match")

    balancesOfEveryone[token] = {
        list(everyone)[i]: balances[i] for i in range(len(list(everyone)))}

    # find contracts with more than global.floorLimit balance and distribute the balance of it using correct plugin
    balancesOfEveryone[token] = distributeContractBals(
        balancesOf=balancesOfEveryone[token])

    if abs(sum(balancesOfEveryone[token].values()) - totSup) > 1e18:
        print(totSup, sum(balancesOfEveryone[token].values()))
        raise Exception("Total Supply and Balances doesn't match")

    balancesOfEveryone[token], blackTokens = applyBlack(
        balancesOfEveryone[token], token)

    expectedTotal = sum(balancesOfEveryone[token].values()) + blackTokens

    if abs(totSup-expectedTotal) > 1e18:  # there is a room for error: 1 tokens!
        raise Exception(
            "blacklist + distributed != totSup", expectedTotal, totSup)

    saveResults(
        dict(sorted(balancesOfEveryone[token].items(),
                    key=lambda item: item[1],
                    reverse=True)),
        token)

    print(f"\n{token.capitalize()} done! in {ceil(time() - start_time)}s")
    print(
        f"distributed {ceil(sum(balancesOfEveryone[token].values())/1e18)} to {len(balancesOfEveryone[token])} addresses")


if __name__ == "__main__":
    tokens = collectTokensData(dataPath='./tokens/')
    for token in tokens:
        snapshot(token)
