# Deployment

See also `docs/deployment.md`.

## Local

```bash
python3.11 -m venv .venv && source .venv/bin/activate
make install
cp .env.example .env
make sandbox
```

## Docker Compose

```bash
docker compose up -d --build
curl http://localhost:8000/healthz
```

## Fly.io

```bash
fly launch --no-deploy
fly secrets set DEEPSEEK_API_KEY=... # optional
fly deploy
```

## Production checklist

- Set `ENVIRONMENT=production`
- Restrict `CORS_ORIGINS` and `TRUSTED_HOSTS`
- Configure `DATABASE_URL` if using persistence
- Set `ADMIN_API_TOKEN`
- Enable Stripe only after testing webhooks in staging
