
from utils.data import collectTokensData

blacklist = collectTokensData(dataPath='./blacklists/')


def filtered(address, balance, token):
    f = balance >= 1e17 and address not in blacklist[token]
    # if not f:
    #     print(address)
    return f


def applyBlack(balances, token):
    print(f"Blacklisting from {len(balances)} address...")
    # make balances of the blacklist zero then delete balances that is less than 1e18
    result = {k: v for k, v in balances.items()
              if filtered(k, v, token)}
    blackTokens = sum(balances.values())-sum(result.values())
    print(f"blacklisted token amount :{blackTokens}")
    return result, blackTokens
