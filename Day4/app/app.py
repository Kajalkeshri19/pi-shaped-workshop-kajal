from flask import Flask, request, jsonify
from vulnerable_module import get_secret_message

app = Flask(__name__)

# -- insecure hardcoded secret (intentional for demo) --
app.config['API_KEY'] = 'SUPER_SECRET_API_KEY_12345'

@app.route('/')
def index():
    return "Hello from vulnerable Flask app!"

# Endpoint that intentionally uses ``eval`` (insecure) to demonstrate Bandit/Semgrep detection
@app.route('/compute')
def compute():
    expr = request.args.get('expr', '1+1')
    # INSECURE: eval on user input (deliberate vulnerability for CI demo)
    result = eval(expr)
    return jsonify({'expr': expr, 'result': result})

@app.route('/secret')
def secret():
    return jsonify({'secret': get_secret_message(), 'api_key': app.config['API_KEY']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
