from flask import Flask, request, render_template, jsonify
from config import SECRET_KEY


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


# Intentionally insecure: DEBUG True and exposing eval on input
app.debug = True


@app.route('/')
def index():
    return render_template('index.html')


# Vulnerable endpoint: executes user input (dangerous)
@app.route('/run', methods=['POST'])
def run_code():
    # Insecure: using eval on user-supplied data
    user_code = request.form.get('code', '')
    try:
        result = eval(user_code)  # INTENTIONAL vulnerability for demo
        return jsonify({'result': str(result)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Hardcoded credentials in source (also in config.py)
@app.route('/secret')
def secret():
    # Example of using a secret in code (should be avoided)
    return jsonify({'secret_key_preview': app.config['SECRET_KEY'][:8] + '...'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)