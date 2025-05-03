from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('miniapp_frontend', 'index.html')

if __name__ == '__main__':
    app.run(port=5000)
