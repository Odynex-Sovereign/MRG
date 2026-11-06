# Procurement / security questionnaire — response outline

Use this as a starting structure when responding to institutional RFPs. Do not invent certifications.

## 1. Product overview

- Purpose: simulation and composure training  
- Data categories: account, simulation activity, technical logs  
- Hosting model options: multi-tenant SaaS, dedicated, customer-hosted  

## 2. Architecture

- Application: FastAPI on Python 3.12  
- Transport: HTTPS; WebSockets for live simulation sessions  
- Secrets: environment / platform secret manager only  

## 3. Access control

- Role concepts: individual, team, organization admin  
- SSO/SAML/OIDC: available when configured for enterprise deployments  
- Audit logs: available on Team+ / institutional packages  

## 4. Encryption

- In transit: TLS (platform-terminated on Fly.io or customer edge)  
- At rest: depends on database and volume provider configuration  

## 5. Operations

- Health checks: `/healthz`, `/readyz`  
- Logging: structured application logs  
- Backups: document process for chosen database provider  

## 6. Compliance posture

- State factually what is implemented  
- Do not claim SOC 2 / ISO / FedRAMP unless independently attested under contract  

## 7. Incident response

- Contact path for security reports  
- Customer notification expectations (define in MSA)  
