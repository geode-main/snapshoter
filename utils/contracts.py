
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
        # print(i, end="\r", flush=True)
        # if isContract(a) and balancesOf[a] > globals.floorLimit:
        if(balancesOf[c] > globals.floorLimit):
            distributed_balances[c] = distributeTokens(
                c, balancesOf[c])

    print(f"\ndone! in {ceil(time() - start_time)}s")
    return distributed_balances


def distributeContractBals(balancesOf):
    distributed_balances = findContracts(balancesOf)

    # print(f"Found contracts : {len(distributed_balances)}")
    # print({k: v for k, v in sorted(contractBals.items(), key=lambda item: item[1],reverse=True)})

    for c in distributed_balances:
        balancesOf[c] = 0
        for a in distributed_balances[c]:
            if a in balancesOf:
                balancesOf[a] += distributed_balances[c][a]
            else:
                balancesOf[a] = distributed_balances[c][a]

    return balancesOf
