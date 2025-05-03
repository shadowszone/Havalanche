from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Temporary in-memory storage (use database in production)
wallet_registry = {}

@app.route("/register", methods=["POST"])
def register_wallet():
    data = request.get_json()
    telegram_id = data.get("telegram_id")
    address = data.get("address")

    if not telegram_id or not address:
        return jsonify({"error": "Missing telegram_id or address"}), 400

    wallet_registry[telegram_id] = address
    return jsonify({"message": "Wallet connected successfully!"}), 200

@app.route("/wallets", methods=["GET"])
def get_all_wallets():
    return jsonify(wallet_registry)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
