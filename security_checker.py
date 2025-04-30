from web3 import Web3
from config import AVALANCHE_RPC_URL

w3 = Web3(Web3.HTTPProvider(AVALANCHE_RPC_URL))

def check_token_risk(address):
    issues = []

    try:
        code = w3.eth.get_code(Web3.to_checksum_address(address))
        if code == b'':
            issues.append("❌ Contract code not found — not deployed?")
        else:
            issues.append("✅ Contract code exists")

        # Add dummy check — real logic needs ABI or source info
        issues.append("⚠️ Ownership renounce not verified (ABI required)")

    except Exception as e:
        issues.append(f"⚠️ Error checking contract: {str(e)}")

    return "🔍 Scam Check:\n" + "\n".join(issues)
