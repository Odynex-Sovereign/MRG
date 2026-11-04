# Operations

## Health

| Endpoint | Use |
|----------|-----|
| `GET /healthz` | Liveness — process up |
| `GET /readyz` | Readiness — dependencies OK |
| `GET /info` | Version and feature flags |

## Logging

- `LOG_FORMAT=json` in production
- Fields include timestamp, level, logger, message; optional request metadata
- Ship stdout to your log stack (CloudWatch, Loki, Datadog, etc.)

## Metrics & tracing

- Enable your preferred OpenTelemetry / Prometheus sidecar or agent
- Application exposes timing via `X-Process-Time-Ms`
- `/metrics` path is reserved in settings for future instrumentation

## Scaling

- Horizontal: increase replicas; ensure LB supports WebSocket sticky sessions if needed
- Vertical: raise machine memory/CPU on Fly or node size on K8s
- Database: connection pool sizes via `DB_POOL_MIN_SIZE` / `DB_POOL_MAX_SIZE`

## Backups

- Use managed Postgres backups or scheduled `pg_dump`
- Application is stateless — no local durable volumes required in production

## Upgrades

1. Run CI green on release branch
2. Apply new migrations if any (`database/run_migrations.py`)
3. Deploy new image
4. Watch `/readyz` and error rates

## Incident response

See [runbook.md](runbook.md).
