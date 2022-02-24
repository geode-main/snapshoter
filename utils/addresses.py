from math import ceil
from time import time
import utils.globals as globals
from web3 import Web3
from multiprocessing import Pool
from itertools import repeat


def _normalize(address):
    # OUTPUT: 0xADDRESS
    return Web3.toChecksumAddress("0x"+address[26:])


def getAddresses(token, fromBlock):
    print(fromBlock, end="\r", flush=True)
    event_logs = []
    addresses = []
    transfer_sig_hash = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"  # transfer
    filterer = {
        'fromBlock': fromBlock,
        'toBlock': fromBlock + globals.step,
        'address': token,
        'topics': [transfer_sig_hash],
    }
    filter = globals.w3.eth.filter(filterer)
    # while loop to get the data even if failed
    counter = 0
    while counter < 10:
        try:
            event_logs = filter.get_all_entries()
            counter = 11
        except:
            if counter < 10:
                counter += 1
            else:
                raise Exception("couldn't get the data...")

    for event in event_logs:
        for i in [1, 2]:
            addresses.append(_normalize(event.topics[i].hex()))
    return list(set(addresses))


def getAllUniqueAddresses(token):
    print("\nReading addresses")
    addresses = set()
    start_time = time()
    print(f"block: {globals.creation} to {globals.snapshot}")
    # threading for multiple requests
    with Pool() as pool:
        M = pool.starmap(getAddresses, zip(
            repeat(token), range(globals.creation, globals.snapshot, globals.step)))
    for result in M:
        addresses.update(result)

    print(f"\ndone! in {ceil(time() - start_time)}s")
    print(f"Unique address count : {len(addresses)}")
    return addresses
