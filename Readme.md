# Cover & Ruler Reimbursement Snapshot

## Results can be found under [results directory](./results/).
> [Google Sheet link for Cover](https://docs.google.com/spreadsheets/d/1jvEuEU3B7autLe3Jd31vjBhN0a8TawfVS9XMIz5MVoo/edit?usp=sharing)

> [Google Sheet link for Ruler](https://docs.google.com/spreadsheets/d/13vLPJ6m_IQc0wamaYXStAipsWjJkHq-GMMYoV16Wfh8/edit?usp=sharing)


## Blacklisted addresses and other important addresses are explained below.

# Setup 

> This repo is compatible with Python3.x

### 1. Create an .env file with your Alchemy api:

```
provider = https://eth-mainnet.alchemyapi.io/v2/<YOUR_ALCHEMY_KEY> 
```

[Api key can be obtained from here.](https://www.alchemy.com/)

### 2. Create a python virtual environment

```
python -m venv <nameOfEnv>
```
### 3. Install Necessary Packages 

```
pip install -r ./requirements.txt
```

### 4. Run script
```
python3 main.py 
```

# Important addresses and Blacklist

## Cover:
| address | balance | importance | STATUS |
|---|---|---|---|
0xc698645B5C5b662B52a5A5C092804F23e3F5B4C5 | 632 | gnosis |
0xE98567885Df519dFeB12C0E268dD5d9b798bD531 | 2157 | vesting  |blacklisted
0x66Ae32178640813F3c32a9929520BFE4Fef5D167 | 2519 | sushiswap | distributed
0x859Eefc267671595d987D0F6589D7771D4877113 | 680 | gnosis |
0x21011BC93d9E515B9511A817A1eD1D6d468f49Fc | 1371 | cream  | distributed
0xa921392015eB37c5977c4Fd77E14DD568c59D5F8 | 12267 | xCover  | distributed
0x15957f0CA310d35b2E73fB5070Ce44A5B0141AB1 | 14262 | gnosis | blacklisted

Total Distributed Cover Amount:


## Ruler:
| address | balance | importance | STATUS |
|---|---|---|---|
0xCe7D2FE4d364C973829195d25b6967087faFd499 | 10708 | vesting  |  blacklisted
0x05927a6DA8D004e9b26CA7aE6e6523470aB02Da4 | 85118 | vesting  | blacklisted
0xFA1F8518d3E6D69A04b88E96a9e3e7588D19cA0c | 286 | airdrop | blacklisted
0x49B8a0893B83A171D7d461198b69A0b1bb4dd0Ed | 190011 | gnosis  | blacklisted
0x3423c8Af3a95D9FEE7Ec06c4e0E905D4fd559F89 | 4826 | ruler rewards pool  | NOT distributed, blacklisted
0x01F7Fd324b366380D2145Dfa6C7A76fdb75f17B9 | 134262 | xRuler  | distributed
0xb1EECFea192907fC4bF9c4CE99aC07186075FC51 | 62502 | sushiswap  | distributed
0xEF0881eC094552b2e128Cf945EF17a6752B4Ec5d | 2500 | sushi(MasterChef) | distributed, blacklisted
0x6BeF09F99Bf6d92d6486889Bdd8A374af151461D | 483610 | gnosis | blacklisted

Total Distributed Ruler Amount: 146994

# Developer Guide

> Expected Run Time: 218 seconds.

The snapshot of the given tokens are taken at the given blockNumber. These data can be found in [tokens folder](./tokens/).
Everything is dynamic, which means any number of ERC20 tokens can be used for snapshots, we are using 2 for this run.

[Utils folder](./tokens/) includes functions to run main script, like finding contracts and distributing their balances.
To make things a lot faster, we used Parallel Processing when necessary.

[Plugins folder](./plugins/) includes contract specific plugins that will detect the type and distribute the balances of given contracts. We have implemented the following plugin types:

- Gnosis: determined by NAME() function call. Simply leaves the balance there.
- xToken: determined by getShareValue() function call. such as xRuler, xCream;  Finds the users of the pool using LPtoken and distributes the balance accordingly.
- Cream: determined by isCToken() function call. such as xRuler, xCream; same method is being used as xToken plugin.
- Sushiswap: determined by factory() function call. same method is being used as xToken plugin; except it also distributes the base tokens for LPtokens in the Masterchef contract(for ruler only rn)

Notes:

- Snapshot will filter out the addresses with less than 1 token.

Output of the last run can be found in [output.txt](./output.txt) 