from plugins.sushiswap.main import detect as sushiswap_detect, distribute as sushiswapdistWeighted
from plugins.gnosis.main import detect as gnosis_detect
from plugins.cream.main import detect as cream_detect, distribute as creamdistWeighted
from plugins.xToken.main import detect as xToken_detect, distribute as xTokendistWeighted
import random

bcolors = ['\033[95m',
           '\033[94m',
           '\033[96m',
           '\033[92m',
           '\033[93m',
           '\033[91m']


def _defaultdistWeighted(address, balance):
    return {address: balance}


def findPlugin(address):
    if gnosis_detect(address):
        print(f"Found plugin: Gnosis")
        return _defaultdistWeighted
    elif sushiswap_detect(address):
        print(f"Found plugin: sushiswap")
        return sushiswapdistWeighted
    elif cream_detect(address):
        print(f"Found plugin: cream")
        return creamdistWeighted
    elif xToken_detect(address):
        print(f"Found plugin: xToken")
        return xTokendistWeighted
    else:
        print(f"NO PLUGIN: default")
        return _defaultdistWeighted


def distributeTokens(contract, balance):
    print(bcolors[random.randint(0, 5)])
    print(f"Contract: {contract}, Balance:{balance}")
    plugin = findPlugin(contract)
    r = plugin(contract, balance)
    print('\033[0m')
    return r
