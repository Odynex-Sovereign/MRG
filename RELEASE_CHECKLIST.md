# Release checklist

- [ ] `make format && make lint && make typecheck && make test-cov` pass locally
- [ ] `docker build -t mrg:release --target production .` succeeds
- [ ] Container `/healthz` returns 200
- [ ] WebSocket smoke (`make smoke`) against running container succeeds
- [ ] `.env.example` updated for any new variables
- [ ] CHANGELOG.md updated
- [ ] No secrets, `.env`, private keys, or credentials in the tree
- [ ] CI green on the release commit
- [ ] Staging deploy verified (`/healthz`, `/readyz`, sample WS session)
- [ ] Production deploy with monitored error rate and rollback plan
