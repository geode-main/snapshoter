def distWeighted(addresses, toDist):
    weight = toDist/sum(addresses.values())
    distributed = {k: v * weight for k,
                   v in addresses.items()}
    return distributed


def valIfExist(k, balances):
    if k in balances:
        return balances[k]
    else:
        return 0


def addWeighted(addresses, balances, toDist):
    weight = toDist/sum(balances.values())
    distributed = {k: v + valIfExist(k, balances) * weight for k,
                   v in addresses.items()}
    return distributed
