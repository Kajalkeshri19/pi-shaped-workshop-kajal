# app/app.py
from flask import Flask, jsonify
import os

app = Flask(__name__)

# DEMO: Hardcoded secret (intentional vulnerability for exercise)
API_KEY = "super-secret-hardcoded-api-key-DO-NOT-USE"

@app.route('/')
def index():
    return jsonify({
        "message": "Hello from vulnerable Flask app",
        "api_key_sample": API_KEY[:6] + "..."  # intentionally expose part of secret for demo
    })

if __name__ == '__main__':
    # Expose on 0.0.0.0:5000 to allow ZAP scanning in CI
    app.run(host='0.0.0.0', port=5000, debug=True)
