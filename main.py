from math import ceil
from time import time
from web3 import Web3
import utils.globals as globals
from utils.data import collectTokensData, saveResults
from utils.addresses import getAllUniqueAddresses
from utils.balances import getBalances
from utils.contracts import distributeContractBals
from utils.blacklist import applyBlack

if __name__ == "__main__":
    tokens = collectTokensData(dataPath='./tokens/')
    for token in tokens:
        print(f"\n{token.capitalize()}:")
        start_time = time()
        balancesOfEveryone = {}
        balancesOfEveryone[token] = {}

        globals.creation = tokens[token]["creation"]
        globals.snapshot = tokens[token]["snapshot"]
        globals.currentToken = globals.w3.eth.contract(
            abi=tokens[token]["abi"], address=Web3.toChecksumAddress(tokens[token]["address"]))

        everyone = getAllUniqueAddresses(
            token=Web3.toChecksumAddress(tokens[token]["address"]), )

        balances = getBalances(everyone)

        if len(everyone) != len(balances):
            raise Exception("address and balances doesn't match")

        balancesOfEveryone[token] = {
            list(everyone)[i]: balances[i] for i in range(len(list(everyone)))}

        # find contracts with more than 100 token balance and distribute the balance of it using correct plugins
        balancesOfEveryone[token] = distributeContractBals(
            balancesOf=balancesOfEveryone[token])

        balancesOfEveryone[token] = applyBlack(
            balancesOfEveryone[token], token)

        saveResults(
            dict(sorted(balancesOfEveryone[token].items(),
                        key=lambda item: item[1],
                        reverse=True)),
            token)

        print(f"\n{token.capitalize()} done! in {ceil(time() - start_time)}s")
        print(
            f"distributed {ceil(sum(balancesOfEveryone[token].values())/1e18)} to {len(balancesOfEveryone[token])} addresses")
