import requests

def get_token_price(coingecko_id: str) -> str:
    url = f"https://coins.llama.fi/prices/current/coingecko:{coingecko_id}"
    try:
        response = requests.get(url).json()
        price = response["coins"][f"coingecko:{coingecko_id}"]["price"]
        return f"💰 {coingecko_id} price: ${price:.4f}"
    except Exception:
        return "⚠️ Could not fetch token price. Make sure the ID is correct."
