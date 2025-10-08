# CI Security Scan Demo — Day 5 Exercise

## Objective
Run automated security scans (SAST, dependency, IaC, container, secrets, DAST) against a sample Flask app and its infrastructure.

## Repo layout
(see repository root)

## Setup steps
1. Clone repo
2. Build and run Docker app: `docker build -t demo-flask-app:latest app && docker run -p 5000:5000 demo-flask-app:latest`
3. Run scans locally (commands in README under "Local steps")
4. Push to GitHub — CI will run automatically.

## Pipeline (GitHub Actions)
Job names:
- bandit (Bandit -> bandit-report.html)
- semgrep (semgrep-report.json)
- trivy-deps (trivy-deps-report.json)
- trivy-docker (trivy-docker-report.json)
- checkov (checkov-report.json)
- gitleaks (gitleaks-report.json)
- zap-dast (zap-report.html)

All artifacts are uploaded and downloadable from the workflow run.

## Scan results (insert screenshots/artifacts)
- Insert screenshots of the GitHub Actions run here.
- Attach or link the artifacts:
    - bandit-report.html
    - semgrep-report.json
    - trivy-deps-report.json
    - trivy-docker-report.json
    - checkov-report.json
    - gitleaks-report.json
    - zap-report.html

## Vulnerabilities (explain at least two)
(Use the two examples above: hardcoded secret, public S3/RDS. Add CVSS if you want.)

## Fix implemented (demonstrated)
- Fixed: removed hardcoded secret from `app/app.py` -> now uses `API_KEY` env var.
- Commit: `<commit-hash>`
- Before/After: include screenshots (before: gitleaks/bandit flagged), after: artifact shows no hardcoded secret finding.

## Scenario-based questions / answers
1. **Why include these scans in CI instead of only after deployment?**
    - Running SAST/DAST and dependency/IaC scans early (shift-left) helps catch issues before release, reduces remediation cost, and prevents vulnerable code/infrastructure from reaching production. Scanning only post-deployment increases blast radius and risk.

2. **Why run Trivy on both dependencies and container images?**
    - Dependency scanning checks vulnerable packages in source (Python packages). Container image scanning detects OS-level and package-level vulnerabilities introduced during image build (base image, system libs). Both give complementary coverage.

3. **How do Bandit, Semgrep, Trivy differ?**
    - Bandit: Python-specific static analyzer focusing on insecure patterns (crypto misuse, hardcoded secrets, insecure SSL usage).
    - Semgrep: pattern-based SAST for many languages — good for custom rules and finding patterns across code.
    - Trivy: vulnerability scanner for filesystem, container images, and IaC; focuses on CVEs in packages and base images.

4. **If a scan fails in pipeline, what should happen?**
    - Ideally: fail the pipeline for high/critical findings; create tickets for triage; block merge until fixed or accepted with documented risk. For low findings, you can allow but schedule remediation.

## Notes
- This repo uses demo/insecure configurations intentionally for training.
- Do NOT deploy the Terraform to production in its current state.

##  Detailed Vulnerabilities & Fixes

---

###  **Vuln 1 — Hardcoded Secret in `app/app.py`**

**Description / Impact:**  
A secret API key was hardcoded in the application source code.  
If the repository is public or ever leaked, attackers can retrieve this secret and use it to access downstream APIs or third-party services.  
This can lead to **data breaches, unauthorized actions, or financial loss** due to exposed credentials.

**Detected by:**
- Bandit (SAST)
- Gitleaks (Secrets Scanner)

**Compliance Risk:**
- Violates **CIS Benchmarks (Secret Management)**
- Violates **NIST SP 800-53: SC-28 (Protection of Information at Rest)**
- Violates **GDPR Article 32** – Security of Processing

**Recommended Fix:**
- Remove all hardcoded secrets from the source code.
- Store secrets securely using **environment variables** or a **secrets manager** like:
    - AWS Secrets Manager
    - HashiCorp Vault
    - GitHub Actions Secrets
- Rotate any exposed secrets immediately and revoke old credentials.

**Demonstrated Fix:**  
Replaced the hardcoded secret with environment-based configuration.
```python
# Before
API_KEY = "super-secret-hardcoded-api-key"

# After
import os
API_KEY = os.environ.get("API_KEY")

## Scenario-Based Questions & Answers

---

### **1. How does each tool contribute to security & compliance (code, infra, dependencies, Docker, secrets, runtime)?**

| Tool | Coverage Area | Security Contribution | Compliance Relevance |
|------|----------------|------------------------|-----------------------|
| **Bandit** | Application code (Python) | Detects insecure coding practices like hardcoded passwords, weak cryptography, unsafe deserialization. | Aligns with **CIS Benchmarks** (secure coding), **NIST SI-10**, **GDPR Art. 25**. |
| **Semgrep** | Pattern-based static analysis | Detects risky code patterns, input validation issues, and injection flaws across languages. | Supports **NIST RA-5 (Vulnerability Scanning)** and **CIS App Security Rules**. |
| **Trivy (Dependencies)** | Python dependency scanning | Identifies vulnerable libraries (CVEs), outdated packages, and unpatched dependencies. | **CIS 3.4**, **NIST SI-2 (Flaw Remediation)**, **GDPR Art. 32** – ongoing vulnerability management. |
| **Checkov** | Infrastructure as Code (Terraform) | Detects misconfigurations like public S3 buckets, open security groups, unencrypted storage. | Directly maps to **CIS AWS Foundations Benchmark**, **NIST AC-4**, and **GDPR Art. 25/32**. |
| **Trivy (Docker Image)** | Container image & OS-level scanning | Finds CVEs in base images, misconfigured packages, and unpatched runtime components. | Ensures **CIS Docker Benchmark** compliance, **NIST CM-6 (Configuration Management)**. |
| **Gitleaks** | Secrets & sensitive data | Detects API keys, passwords, tokens in commits and history to prevent leaks. | Critical for **GDPR compliance (data protection by design)** and **CIS Secret Management**. |
| **OWASP ZAP** | Runtime / DAST scanning | Identifies real-time web app vulnerabilities such as XSS, SQLi, CSRF, and missing security headers. | Covers **OWASP Top 10**, **NIST RA-5**, **GDPR Art. 32** for system protection during processing. |

✅ Together, these tools provide **end-to-end DevSecOps coverage** — from **code to cloud runtime**, ensuring compliance with **CIS**, **NIST 800-53**, and **GDPR** security standards.

---

### **2. Pick one critical vulnerability: exploitation, business impact, and remediation**

**Vulnerability Chosen:** Hardcoded Secret in `app/app.py`

**Exploitation Path:**
1. Attacker finds the hardcoded API key from the public GitHub repository.  
2. The key is reused to authenticate with external APIs or internal microservices.  
3. The attacker can perform malicious actions such as reading sensitive data, modifying configurations, or launching API-based DoS attacks.

**Business Impact:**
- Unauthorized access leading to **data breach**.  
- Potential **GDPR non-compliance** (Articles 25 & 32) due to poor data protection controls.  
- **Financial loss** or service disruption if the API key is tied to paid services.  
- **Reputation damage** if customer data is exposed.

**Remediation:**
- Remove hardcoded secret and store it securely using environment variables or a secrets manager.  
- Rotate exposed key immediately.  
- Apply least-privilege permissions to new API keys.  
- Enforce secret scanning via **Gitleaks** in CI/CD to prevent recurrence.  

✅ After fix, Bandit and Gitleaks reported **no findings**, verifying compliance and risk mitigation.

---

###  **3. How to prioritize fixes when multiple issues are reported?**

Prioritization should balance **severity**, **compliance impact**, and **ease of remediation**:

| Priority | Criteria | Example |
|-----------|-----------|----------|
| **P1 – Critical** | High CVSS score (>9.0), public exposure, or secret leakage. Immediate compliance risk (GDPR/CIS). | Hardcoded secret, Public S3 bucket |
| **P2 – High** | Vulnerabilities enabling RCE, privilege escalation, or major data access issues. | Outdated dependency with CVE |
| **P3 – Medium** | Non-compliant but low-exposure misconfigs or insecure defaults. | Missing encryption-at-rest flag |
| **P4 – Low** | Informational, best-practice issues with minimal impact. | Missing tags or metadata in IaC |

 **Remediation Strategy:**
1. Fix P1 issues **immediately** and fail builds automatically for them.  
2. Automate dependency updates (Trivy, Dependabot).  
3. Address medium findings iteratively during sprints.  
4. Document and monitor low-priority issues to maintain compliance posture.

---

###  **4. How do Checkov findings map to frameworks like CIS AWS / NIST / GDPR? Provide one real example.**

**Example Finding:**  
```hcl
resource "aws_s3_bucket" "public_bucket" {
  bucket = "my-data"
  acl    = "public-read"
}

###  **5. Why are both ZAP (runtime) and Trivy (image scan) needed? What unique gaps does each fill?**

**Purpose:**  
Both tools serve different but complementary roles in securing an application — one before deployment (Trivy) and one after deployment (ZAP).

| Tool | Scan Type | Primary Focus | Security Layer | Unique Capability | Gap it Fills |
|------|------------|----------------|----------------|--------------------|---------------|
| **Trivy** | Static / Pre-deployment | Scans application dependencies, Docker images, and OS-level packages for known CVEs and misconfigurations. | **Build-time / Image layer** | Detects vulnerabilities in the application’s base image, libraries, and infrastructure components. | Ensures the container image is free from known vulnerabilities **before it’s deployed**. |
| **OWASP ZAP** | Dynamic / Runtime | Actively probes the running web application to find exploitable vulnerabilities like XSS, SQL Injection, CSRF, and authentication flaws. | **Runtime / Application layer** | Simulates real-world attacks to validate how the app behaves when deployed. | Detects vulnerabilities **that only appear during execution**, which static scans cannot find. |

**Why both are essential:**
-  **Trivy ensures you build securely** — it prevents known vulnerabilities from entering your container image or dependencies.  
-  **ZAP ensures you run securely** — it validates that the deployed application resists runtime exploitation.  
-  **Together**, they provide full **Defense-in-Depth** coverage across the software lifecycle:
- **Trivy** → Secure Image & Dependencies  
- **ZAP** → Secure Deployed Application

**Compliance Relevance:**
- **NIST SP 800-53: RA-5 & SI-2** – Continuous vulnerability scanning & flaw remediation.  
- **CIS Docker Benchmark** – Secure container configuration.  
- **GDPR Article 32** – Ongoing security of processing and protection by design.

---


