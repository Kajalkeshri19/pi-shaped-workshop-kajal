# Simple module that holds a secret — used to demonstrate secret-detection tools
def get_secret_message():
    # deliberate hardcoded secret (to be detected by Gitleaks/CI scanning)
    return "my-module-secret-98765"
