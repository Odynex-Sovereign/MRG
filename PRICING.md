# Pricing

**Single source of truth:** `mrg/pricing.py`

Checkout is **demo mode** by default. No live charges occur until Stripe is connected.

## Public plans (USD)

| Plan ID | Name | Monthly | Annual | Trial | Notes |
|---------|------|---------|--------|-------|-------|
| `free` | Sandbox | $0 | $0 | — | Forever free, limited minutes |
| `starter` | Starter | $49 | $470 | 14 days | Individual practitioners |
| `growth` | Growth | $499 | $4,790 | 14 days | Teams up to 10 seats |
| `enterprise` | Enterprise | Custom | Custom | — | Contact sales |

### Billing rules (product language)

- Currency: **USD**
- Cadence: monthly or annual (annual ≈ 20% discount on Starter/Growth)
- Renewals: automatic until canceled
- Taxes: calculated at checkout when payment provider is live
- Cancellation: anytime; access continues through the paid period
- Enterprise: custom contracts, SSO, SLA, DPA

## Enterprise modules (indicative)

Defined in `ENTERPRISE_MODULES` inside `mrg/pricing.py` (e.g. Molecular SaaS $15,000/mo, Platinum CAVE $160,000/mo). These are **not** self-serve; rates are planning placeholders from the historical catalog.

## Where pricing appears

- `/pricing` — plan cards + enterprise table (loaded from `/api/pricing`)
- `/checkout` — demo checkout bound to `plan` + `interval` query params
- `/` — summary CTAs
- `/api/pricing`, `/api/pricing/{id}`, `/api/checkout/demo`
- README and this file

## Editing prices

1. Edit `mrg/pricing.py` (`PUBLIC_PLANS` / `ENTERPRISE_MODULES`)
2. Restart the app
3. Confirm `/api/pricing` and the pricing page

## Connecting Stripe (production)

1. Set `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `STRIPE_PUBLISHABLE_KEY`
2. Set `ENABLE_BILLING=true`
3. Create Stripe Products/Prices matching plan IDs
4. Replace demo path in `mrg/api/pricing.py` (`demo_checkout`) with Checkout Session creation (see `services/billing/checkout_engine.py` for prior art)
5. Handle `customer.subscription.*` webhooks
6. Remove or gate the "Demo checkout" banner in `app/checkout.html`

Until then, UI and API clearly label demo behavior.
