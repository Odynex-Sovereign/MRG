# Deployment

## Local production-like

```bash
cp .env.example .env
# set POSTGRES_* and optional API keys
docker compose up -d --build
docker compose exec mrg python database/run_migrations.py
curl http://localhost:8000/healthz
curl http://localhost:8000/readyz
```

## Fly.io

1. Install `flyctl` and authenticate
2. `fly launch --no-deploy` (uses existing `fly.toml`)
3. Set secrets: `fly secrets set DEEPSEEK_API_KEY=… NVIDIA_NIM_API_KEY=…`
4. Optionally attach a Postgres cluster and set `DATABASE_URL`
5. `fly deploy`
6. Verify: `fly status`, `curl https://<app>.fly.dev/healthz`

CI deploys on push to `main` when `FLY_API_TOKEN` is configured as a repository secret.

## Kubernetes

Example manifests live under `deploy/k8s/`:

- Deployment with liveness `/healthz` and readiness `/readyz`
- Service
- Optional ConfigMap / Secret references (no plaintext secrets in git)

Apply with `kubectl apply -f deploy/k8s/` after filling Secret values via your preferred secret manager.

## Terraform

`deploy/terraform/` provides a minimal module skeleton. Cloud credentials must be supplied out-of-band (OIDC, env vars). Do not commit `terraform.tfvars` with secrets.

## Rollback

- Fly: `fly releases` then `fly deploy --image <previous>`
- K8s: roll back Deployment revision
- Images should be tagged immutably in CI for safe rollback
