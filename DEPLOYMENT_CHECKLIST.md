# Deployment options checklist

## A. Multi-tenant SaaS (default)

- [ ] Fly app created  
- [ ] Secrets set (`SECRET_KEY`, optional Stripe, optional DB)  
- [ ] Custom domain + TLS  
- [ ] Health checks green  
- [ ] Backup plan for any persistent volume / database  

## B. Dedicated Fly / cloud instance

- [ ] Separate Fly app or project  
- [ ] Region / residency agreed  
- [ ] Network restrictions if required  
- [ ] Admin access handoff  
- [ ] Monitoring and log retention agreed  

## C. Customer-hosted

- [ ] Container image supply method  
- [ ] Minimum runtime (Python 3.11+, or prebuilt image)  
- [ ] Environment variable contract reviewed  
- [ ] Ingress TLS and WebSocket support confirmed  
- [ ] Update channel defined  

## Common

- [ ] Pricing / order form signed  
- [ ] Support contact named  
- [ ] Acceptance criteria agreed  
