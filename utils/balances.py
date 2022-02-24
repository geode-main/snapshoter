import utils.globals as globals
from multiprocessing import Pool
from time import time
from math import ceil


def getAddressBalance(address):
    print(address, end="\r", flush=True)
    return globals.currentToken.functions.balanceOf(address).call(block_identifier=globals.snapshot)


def getBalances(addresses):
    print("\nReading balances")
    start_time = time()
    with Pool() as pool:
        BALANCES = pool.starmap(getAddressBalance, zip(list(addresses)))
    print(f"\ndone! in {ceil(time() - start_time)}s")
    totSup = globals.currentToken.functions.totalSupply().call(
        block_identifier=globals.snapshot)
    sumSup = sum(BALANCES)
    print(f"TotSup:{totSup} -> Found:{sumSup}")
    if not sumSup == totSup:
        raise Exception("Total Supply and Balances doesn't match:")
    return BALANCES
