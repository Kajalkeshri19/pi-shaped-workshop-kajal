
# CI/CD-Based DevSecOps Pipeline – Tools & Integrations

This repository demonstrates a vulnerable Flask app with a CI/CD pipeline that runs:

* Bandit (detect insecure Python patterns)
* Semgrep (insecure coding patterns)
* Trivy (vulnerable dependencies)
* OWASP ZAP (DAST runtime scanning)

## Short Description of Vulnerabilities

### 1. Insecure use of `eval()` in `app/app.py`

* **Impact:** Allows attackers to execute arbitrary Python code via user input, leading to potential remote code execution.
* **Fix:** Replace `eval()` with `ast.literal_eval()` or a safe parser to restrict execution to literals only.

### 2. Hardcoded secrets in `app/vulnerable_module.py` and `app/app.py`

* **Impact:** Exposes sensitive API keys or credentials that can be exploited if the source code is accessed.
* **Fix:** Remove hardcoded secrets and use environment variables or a secrets manager.

## Pipeline Integration

### Importance of running Trivy scans in CI/CD

Running Trivy scans in the CI/CD pipeline detects vulnerabilities in OS packages and dependencies before deployment. Relying only on post-deployment scans risks introducing vulnerable packages into production, making early detection and remediation critical for security.

### Importance of running security scans (SAST, dependency scanning, DAST) in CI/CD

Performing security scans directly in CI/CD ensures vulnerabilities are caught during development, not in production. This provides immediate feedback to developers, reduces risk of security incidents, and lowers remediation costs.

## Tool Roles & Complementarity

| Tool          | Role in Pipeline              | Unique Detection Example                                  |
| ------------- | ----------------------------- | --------------------------------------------------------- |
| **Bandit**    | SAST (static Python analysis) | Detects unsafe `eval()` usage.                            |
| **Semgrep**   | SAST with custom rules        | Detects hardcoded secrets in code.                        |
| **Trivy**     | Dependency scanning           | Detects CVEs in outdated Flask or requests packages.      |
| **OWASP ZAP** | DAST (runtime scanning)       | Detects missing security headers and debug mode exposure. |

## Developer Actionability

* **Trivy HIGH severity vulnerability:** Update the base image or dependencies to secure versions, rebuild, and rerun CI scans.
* **Bandit hardcoded secrets:** Remove secrets from code, use environment variables or a secret manager, and rerun CI to confirm resolution.

