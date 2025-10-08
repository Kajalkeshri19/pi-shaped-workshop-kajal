# app/app.py (fixed)
from flask import Flask, jsonify
import os

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY", "<not-set>")  # use env var

@app.route('/')
def index():
    return jsonify({
        "message": "Hello from fixed Flask app",
        "api_key_sample": API_KEY[:6] + "..." if API_KEY else "none"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

