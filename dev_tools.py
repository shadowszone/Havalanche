import requests
from web3 import Web3
from config import AVALANCHE_RPC_URL, SNOWTRACE_API_KEY

w3 = Web3(Web3.HTTPProvider(AVALANCHE_RPC_URL))

def get_abi(address):
    url = f"https://api.snowtrace.io/api?module=contract&action=getabi&address={address}&apikey={SNOWTRACE_API_KEY}"
    response = requests.get(url).json()
    return response["result"]

def read_method(address, method_name):
    abi = get_abi(address)
    contract = w3.eth.contract(address=address, abi=abi)
    method = getattr(contract.functions, method_name)
    return method().call()
