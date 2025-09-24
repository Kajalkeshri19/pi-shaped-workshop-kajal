# DevSecOps Hands-On: Code Security & Shift-Left Practices

## Objective

Demonstrate understanding of **shift-left security principles** by scanning code for secrets, safely removing them, and deploying a Node.js application securely.

---

## Project Overview

This project contains a sample Node.js application that loads secrets from a `.env` file. The goal is to:

1. Detect secrets in code using **Gitleaks**
2. Remove hardcoded secrets
3. Secure secrets via environment variables
4. Run the application locally or in Docker
5. Document findings and lessons learned

---

## Steps Taken

### 1️⃣ Setup Project

```bash
mkdir DevSecOp_Assignement_Day1
cd DevSecOp_Assignment_Day1
npm init -y
npm install dotenv
touch .env
echo ".env" >> .gitignore
```

* Created `.env` file for secrets (GITHUB\_PAT, API\_KEY)
* Added `.env` to `.gitignore` to avoid committing secrets

---

### 2️⃣ Create Sample Application
// app.js


---

### 3️⃣ Initialize Git

```bash
git init
git add .
git commit -m "Initial commit - environment variables configured"
```

* Ensured no secrets are hardcoded in code
* `.env` remains local and is ignored by Git

---

### 4️⃣ Install Gitleaks

```bash
wget https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks_Linux_x64.tar.gz
tar -xzf gitleaks_Linux_x64.tar.gz
sudo mv gitleaks /usr/local/bin/
```

* Verify with:

```bash
gitleaks --version
```

---

### 5️⃣ Run Gitleaks Scan

```bash
gitleaks detect --source . --report-format json --report-path gitleaks_report.json
```

**Findings:**

* Initial scan after committing secrets may detect leaks (if secrets were previously committed)
* After moving secrets to `.env` and updating Git history, **Gitleaks shows 0 leaks**

**Screenshots to capture:**

1. Gitleaks scan **before** removing hardcoded secrets
2. Gitleaks scan **after** securing secrets in `.env`

---

### 6️⃣ Run Application

```bash
node app.js
```

Expected output:

```
Starting DevSecOps demo app...
Loaded secrets from environment:
API_KEY: ****
App running...
```

---

### 7️⃣ Docker Deployment (Optional)

**Dockerfile:**

```dockerfile
FROM node:20
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["node", "app.js"]
```

**Build and run:**

```bash
docker build -t devsecops-node-demo .
docker run -p 5000:5000 --env-file .env devsecops-node-demo
```

---

## Core Concepts Learned

1. **Shift-left security**: Move security checks earlier in development to reduce vulnerabilities.
2. **Detecting secrets early**: Prevents accidental leaks of API keys, tokens, or credentials in production.
3. **Storing secrets securely**: Use environment variables, secret managers, or vaults instead of hardcoding secrets.
4. **Residual risk**: Secrets in Git history require cleanup and rotation.

---

## Lessons Learned

* Always **ignore `.env` files** in Git.
* Gitleaks is reliable for automated secret detection.
* Dockerized apps must load secrets via `--env-file` or environment variables.
* Hardcoded secrets in Git history require `git filter-branch` or **BFG Repo Cleaner**.
* Shift-left practices improve security awareness early in development.

---

## Conclusion

This workflow ensures:

* Code security before deployment
* Removal of hardcoded secrets
* Safe deployment with protected secrets
* Integration of Gitleaks scans into CI/CD pipelines for automated secret detection
