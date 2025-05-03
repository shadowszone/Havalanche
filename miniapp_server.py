from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wallets.db'  # Use SQLite to store wallets
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Wallet Model: Store Telegram ID and associated wallet address
class Wallet(db.Model):
    telegram_id = db.Column(db.String(50), primary_key=True)
    address = db.Column(db.String(255), nullable=False)

    def __init__(self, telegram_id, address):
        self.telegram_id = telegram_id
        self.address = address

    def to_dict(self):
        return {"telegram_id": self.telegram_id, "address": self.address}

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register_wallet():
    data = request.get_json()
    telegram_id = data.get('telegram_id')
    address = data.get('address')

    if not telegram_id or not address:
        return jsonify({"message": "Telegram ID and address are required!"}), 400

    # Check if wallet already exists
    existing_wallet = Wallet.query.get(telegram_id)
    if existing_wallet:
        existing_wallet.address = address  # Update existing address
        db.session.commit()
        return jsonify({"message": f"Wallet address updated for Telegram ID {telegram_id}."})

    # Create new wallet entry
    new_wallet = Wallet(telegram_id=telegram_id, address=address)
    db.session.add(new_wallet)
    db.session.commit()

    return jsonify({"message": "Wallet registered successfully!"})

@app.route('/wallets', methods=['GET'])
def get_wallets():
    wallets = Wallet.query.all()
    return jsonify([wallet.to_dict() for wallet in wallets])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
