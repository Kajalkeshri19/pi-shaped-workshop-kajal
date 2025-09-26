# DevSecOps Hands-On: Code Security & Shift-Left Practices  

## Objective  
This project demonstrates the integration of **OWASP ZAP (Zed Attack Proxy)** into a CI/CD pipeline to perform automated security scans on the **OWASP Juice Shop** application. 
The goal is to: 
- Identify vulnerabilities. 
- Map them to the **OWASP Top 10** categories. 
- Propose actionable fixes to secure the application. 

---

##  Tools & Technologies  
- **Application:** OWASP Juice Shop 
- **Security Tool:** OWASP ZAP 
- **CI/CD Platform:** GitHub Actions 

---

# OWASP Juice Shop Security Scan with OWASP ZAP

This guide demonstrates how to run OWASP Juice Shop locally and perform a security scan using OWASP ZAP.

## Prerequisites

- Docker installed and running
- Basic knowledge of running Docker containers
- Access to CI/CD platform (GitHub Actions example provided)


## 1. Start OWASP Juice Shop

Run Juice Shop locally on port 3000:

docker run -d --name juice-shop -p 3000:3000 bkimminich/juice-shop

Verify it’s running:

curl http://localhost:3000


##  Vulnerability Identification & Analysis

### 1. Absence of Anti-CSRF Tokens  
- **OWASP Category:** A01:2021 – Broken Access Control 
- **Impact:** Attackers can trick authenticated users into performing unintended actions (e.g., fund transfers, password changes). 
- **Fix:** 
  - Implement CSRF tokens for all state-changing requests. 
  - Use framework-provided CSRF protection (`Django`, `Spring Security`, `Express.js + csurf`). 
  - Ensure tokens are unique per session and validated server-side. 

---

### 2. Content Security Policy (CSP) Header Not Set  
- **OWASP Category:** A05:2021 – Security Misconfiguration 
- **Impact:** Without CSP, browsers cannot restrict scripts/resources, increasing the risk of **Cross-Site Scripting (XSS)** and data injection attacks. 
- **Fix:** 
  - Apply a strict **CSP header**, for example: 

    ```http
    Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-<random>'; object-src 'none'; frame-ancestors 'none';
    ```

  - Start with `Content-Security-Policy-Report-Only` mode to monitor violations. 
  - Avoid `unsafe-inline` and `unsafe-eval`. 
  
  

## Core Concept Questions

### 1. What is the purpose of DAST and how does it complement other security testing methods?
**DAST (Dynamic Application Security Testing)** is a type of security testing that analyzes a running application to identify vulnerabilities from an external perspective. Unlike **SAST (Static Application Security Testing)**, which inspects source code, DAST tests the application in real-time, simulating attacks such as SQL injection, XSS, and other vulnerabilities that occur during runtime. DAST complements other security testing methods by providing insight into security weaknesses that may not be visible in the source code and ensuring that deployed applications are secure against external threats.

---

### 2. Explain how XSS or SQL injection vulnerabilities can affect an application and its users.
- **XSS (Cross-Site Scripting):** This vulnerability allows attackers to inject malicious scripts into web pages viewed by other users. Consequences include session hijacking, data theft, phishing attacks, or defacement of the application.
- **SQL Injection:** This vulnerability occurs when user input is improperly sanitized and is executed as part of SQL queries. It can lead to unauthorized access, data leakage, data modification, or complete compromise of the database.

Both vulnerabilities can significantly harm both the application’s integrity and the privacy/security of its users.

---

### 3. Describe the steps you would take to fix the vulnerabilities detected in your ZAP scan.
1. **Identify Vulnerabilities:** Review ZAP scan reports to understand each detected issue.
2. **Prioritize Fixes:** Address critical vulnerabilities first (e.g., SQL injection, XSS).
3. **Implement Fixes:**
   - Use parameterized queries or ORM tools to prevent SQL injection.
   - Validate and sanitize user inputs to prevent XSS.
   - Apply proper authentication, authorization, and security headers.
4. **Retest:** Run ZAP scans again to verify that vulnerabilities are fixed.
5. **Document & Monitor:** Keep track of fixes and monitor for new vulnerabilities in future releases.

---

### 4. How does integrating ZAP scans into CI/CD pipelines support shift-left security practices?
Integrating ZAP scans into CI/CD pipelines ensures that security testing is performed automatically with every build or deployment. This **shift-left** approach detects vulnerabilities early in the development lifecycle, reducing the cost and effort required to fix security issues. Early detection prevents insecure code from reaching production, strengthens application security, and promotes a culture of proactive security awareness among developers.

---











