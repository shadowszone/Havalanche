import requests
from config import SNOWTRACE_API_KEY

def check_token_risk(address):
    url = f"https://api.snowtrace.io/api?module=contract&action=getsourcecode&address={address}&apikey={SNOWTRACE_API_KEY}"
    data = requests.get(url).json()["result"][0]

    issues = []
    if not data["SourceCode"]:
        issues.append("❌ Contract not verified")
    if "Ownable" in data["ABI"] and "renounceOwnership" not in data["SourceCode"]:
        issues.append("❌ Ownership not renounced")

    return "🔍 Scam Check:\n" + "\n".join(issues) if issues else "✅ No obvious red flags"
