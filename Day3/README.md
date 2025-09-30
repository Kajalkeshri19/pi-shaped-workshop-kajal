# Vulnerable Flask Demo + CI/CD Security Scans

## Overview

This project demonstrates a vulnerable Python Flask application with CI/CD security scanning using Bandit, Semgrep, Gitleaks, and OWASP ZAP. The purpose is to identify common security issues, generate reports as artifacts, and show how fixes affect scan results.

## Pipeline Steps

1. **Bandit**: Scans Python code for common security issues and generates `bandit-report.html`.
2. **Semgrep**: Detects additional insecure coding patterns and outputs `semgrep-report.json`.
3. **Gitleaks**: Detects hardcoded secrets, outputs `gitleaks-report.json`.
4. **OWASP ZAP**: Performs a DAST scan of the running app, generating `zap-report.html` and `zap-report.json`.

## Example Vulnerabilities Found

### 1. Use of `eval()` on user input (Bandit)

* **Impact**: Arbitrary code execution. An attacker can run Python code on the server, potentially taking full control.
* **Recommended Fix**: Avoid using `eval()` on user input. Use safe parsers or controlled logic.
* **Evidence of Fix**: Commented out the `eval()` line in `app.py`. After rerunning the pipeline, Bandit no longer flags this vulnerability.

### 2. Hardcoded secret key in `config.py` (Gitleaks)

* **Impact**: Secrets exposed in source code can be leaked, allowing attackers to forge cookies or bypass authentication.
* **Recommended Fix**: Move secrets to environment variables or a secure secrets manager. Do not hardcode them in source code.
* **Evidence of Fix**: Not applied in this demo; report still flags the hardcoded secret.

## How to Run Locally

1. Activate virtual environment: `source .venv/bin/activate`
2. Install requirements: `pip install -r requirements.txt`
3. Run the app: `python app.py`
4. Trigger scans via GitLab CI by committing and pushing changes.

## Observed Pipeline Reports

* **Bandit Report**: Shows `eval()` use and debug mode in Flask app.
* **Semgrep Report**: Detects insecure function usage patterns.
* **Gitleaks Report**: Flags `SECRET_KEY` in `config.py`.
* **OWASP ZAP Report**: Missing HTTP security headers, information disclosure.

## Fix & Validation

* Issue fixed: Disabled debug mode and removed `eval()`.
* Pipeline rerun validated that Bandit no longer reports debug mode or `eval()` as vulnerabilities.

## Scenario-Based Answers

1. **Shift-Left Security**: Detecting vulnerabilities early in CI/CD prevents production issues and reduces remediation cost.
2. **Detecting Secrets Early**: Using Gitleaks prevents leaking sensitive keys in the repository.
3. **Secure Storage of Secrets**: Use environment variables, secret managers (like Vault or AWS Secrets Manager), and avoid hardcoding.
4. **Remaining Risks**: Even after scanning, secrets could be exposed in logs or backups. Mitigate by auditing storage and access.

## Core Concept Questions

### 1. Difference between SAST, DAST, and Secrets Scanning

* **SAST (Static Application Security Testing)**: Analyzes source code for vulnerabilities without executing the program (e.g., Bandit, Semgrep).
* **DAST (Dynamic Application Security Testing)**: Scans the running application for runtime vulnerabilities (e.g., OWASP ZAP).
* **Secrets Scanning**: Detects hardcoded secrets in the code repository (e.g., Gitleaks).
* **Why all three**: Using SAST, DAST, and secrets scanning together ensures comprehensive security coverage at multiple layers in the CI/CD pipeline.

### 2. Why storing secrets in code is dangerous and secure alternatives

* **Danger**: Hardcoded secrets can be leaked via the repo, logs, or backups, giving attackers unauthorized access.
* **Secure alternative**: Store secrets in environment variables or secret management tools like HashiCorp Vault, AWS Secrets Manager, or Kubernetes Secrets.

### 3. How adding scans helps enforce Shift-Left Security

* **Explanation**: Integrating security scans into CI/CD early (Shift-Left) detects vulnerabilities and misconfigurations before code reaches production, reducing cost and risk.

### 4. Next step if a scan fails

* **Action**: Developer/DevOps should review the report, fix the identified issue(s), and commit/push the changes. Then rerun the pipeline to validate the fix before merging/deploying.
