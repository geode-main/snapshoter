def distWeighted(addresses, toDist):
    weight = toDist/sum(addresses.values())
    distributed = {k: v * weight for k,
                   v in addresses.items()}
    return distributed
