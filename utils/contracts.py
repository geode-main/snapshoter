
import utils.globals as globals
from plugins.plugins import distributeTokens
from multiprocessing import Pool
from time import time
from math import ceil


def isContract(a):
    print(a, end="\r", flush=True)
    code = None
    counter = 0
    while code is None:
        try:
            code = globals.w3.eth.getCode(a)
        except:
            if counter < 10:
                counter += 1
            else:
                raise Exception("couldn't get the data...")

    return a if code != b'' else "0x0000000000000000000000000000000000000000"


def findContracts(balancesOf):
    print("\nFinding contracts")
    start_time = time()
    distributed_balances = {}
    with Pool() as pool:
        contractBoolMap = pool.starmap(
            isContract, zip(list(balancesOf.keys())))
    contracts = set(contractBoolMap)
    print(f"\n{len(contracts)} contracts found in {ceil(time() - start_time)}s")

    for c in contracts:
        if(balancesOf[c] > globals.floorLimit):
            distributed_balances[c] = distributeTokens(
                c, balancesOf[c])

    print(f"\ndone! in {ceil(time() - start_time)}s")
    return distributed_balances


def distributeContractBals(balancesOf):
    distributed_balances = findContracts(balancesOf)
    cBal = sum(balancesOf.values())

    for c in distributed_balances:  # do not override in a for loop: seperated: plugins can pay other plugins
        balancesOf[c] = 0

    for c in distributed_balances:
        for a in distributed_balances[c]:
            if a in balancesOf:
                balancesOf[a] = balancesOf[a] + distributed_balances[c][a]
            else:
                balancesOf[a] = distributed_balances[c][a]
    return balancesOf
