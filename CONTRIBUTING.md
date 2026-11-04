# Contributing to MRG

Thank you for contributing.

## Development setup

1. Fork and clone the repository
2. `python3.11 -m venv .venv && source .venv/bin/activate`
3. `make install`
4. `cp .env.example .env`
5. `make test`

## Code standards

- Python 3.11+, type hints where practical
- Format and lint with `make format && make lint`
- Type-check with `make typecheck`
- Add or update tests for behavioral changes
- Do not commit secrets, `.env`, or large binaries

## Pull requests

- Target `main`
- Keep changes focused
- Ensure CI is green
- Update CHANGELOG.md under an Unreleased section when appropriate

## Security

See [SECURITY.md](SECURITY.md) for vulnerability reporting. Do not discuss unfixed vulnerabilities in public PRs.
