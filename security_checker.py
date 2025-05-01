import requests
from web3 import Web3
from config import AVALANCHE_RPC_URL

w3 = Web3(Web3.HTTPProvider(AVALANCHE_RPC_URL))


def fetch_contract_abi(address):
    url = "https://api.routescan.io/v2/network/mainnet/evm/avalanche/etherscan/api"
    params = {
        "module": "contract",
        "action": "getabi",
        "address": address,
        "apikey": ""  # Leave blank for free tier
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data.get("status") == "1":
            return data["result"]
        else:
            return None
    except Exception as e:
        return None


def check_token_risk(address):
    issues = []

    try:
        checksum_address = Web3.to_checksum_address(address)
        code = w3.eth.get_code(checksum_address)
        if code == b'':
            issues.append("❌ Contract code not found — not deployed?")
            return "🔍 Scam Check:\n" + "\n".join(issues)
        else:
            issues.append("✅ Contract code exists")

        abi_json = fetch_contract_abi(address)
        if not abi_json:
            issues.append("⚠️ ABI fetch failed — ownership renounce not verified")
        else:
            contract = w3.eth.contract(address=checksum_address, abi=abi_json)
            try:
                owner = contract.functions.owner().call()
                if owner == "0x0000000000000000000000000000000000000000":
                    issues.append("✅ Ownership renounced")
                else:
                    issues.append(f"⚠️ Contract still owned by {owner}")
            except Exception:
                issues.append("⚠️ 'owner()' method not found — can't verify renounce")

    except Exception as e:
        issues.append(f"⚠️ Error checking contract: {str(e)}")

    return "🔍 Scam Check:\n" + "\n".join(issues)
