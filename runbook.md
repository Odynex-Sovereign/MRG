# Runbook

## Service will not start

1. Check logs: `docker compose logs mrg` or `fly logs`
2. Confirm Python package import: `python -c "from mrg.app import app"`
3. Verify `PORT` and binding `0.0.0.0`
4. Ensure `tini` / entrypoint not overridden incorrectly

## `/readyz` returns 503

- Database configured but unreachable — verify `DATABASE_URL`, network, credentials
- Temporarily omit `DATABASE_URL` to run sandbox-only

## WebSocket disconnects immediately

- Proxy must support WebSocket upgrade (Fly, nginx `proxy_http_version 1.1`, etc.)
- Check message size vs `MAX_MESSAGE_SIZE_BYTES`
- Validate client JSON against `TelemetryPacket`

## High latency on macro responses

- DeepSeek timeouts fall back automatically
- Increase `DEEPSEEK_TIMEOUT_SECONDS` or reduce prompt size
- Sandbox mode is local and fast — use it to isolate network issues

## Deploy failed on Fly

- Confirm `FLY_API_TOKEN` secret in GitHub Actions
- Run `fly deploy` locally with the same `fly.toml`
- Check region capacity and app name uniqueness

## Rollback

```bash
fly releases
fly deploy --image registry.fly.io/<app>:<previous-tag>
```

Or redeploy the previous git SHA from CI.
