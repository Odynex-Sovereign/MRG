# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 1.1.x   | Yes       |
| 1.0.x   | Best effort |

## Reporting a vulnerability

Please report security issues privately. Do **not** open public GitHub issues for vulnerabilities that could be exploited.

Email the maintainers at the contact listed in the repository or organization profile, or open a private security advisory on GitHub if enabled.

Include:

- Description of the issue
- Steps to reproduce
- Affected versions / commit
- Any known mitigations

You should receive an acknowledgment within a few business days.

## Security practices in this project

- Secrets only via environment / platform secret managers
- Dependency versions pinned; review `requirements.txt` on upgrade
- Containers run as non-root
- Input validation on API and WebSocket payloads
- Security response headers on HTTP responses
- Optional database integration; core path works without it

## Scope

In scope: the MRG application code, Docker images, and deployment manifests in this repository.

Out of scope: third-party APIs (DeepSeek, NVIDIA, Stripe, Livepeer), user-operated infrastructure misconfiguration, and denial-of-service against public endpoints without prior coordination.
