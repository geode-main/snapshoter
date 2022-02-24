from os import getenv
from dotenv import load_dotenv
from web3 import Web3, HTTPProvider
load_dotenv()

w3 = Web3(HTTPProvider(getenv('provider')))
currenToken = None
creation = None
snapshot = None
floorLimit = 100e18
step = 10000
