# Pricing and checkout

The landing page offers three monthly subscription tiers:

| Tier ID | Plan | Monthly USD |
|---------|------|-------------|
| `tier_1` | Molecular SaaS | $15,000 |
| `tier_2` | Infrastructure Base | $35,000 |
| `tier_3` | Platinum CAVE | $160,000 |

Checkout is served by the same FastAPI application as the landing page at `POST /billing/v1/checkout/create-session`. The browser submits only the tier ID; prices are selected and enforced server-side. When Stripe is not configured, the API reports sandbox mode and never claims a payment succeeded.

## Enable live Stripe Checkout

1. Revoke any Stripe secret or restricted key that has been pasted into chat, committed, or otherwise exposed. Create a replacement key in Stripe after reviewing its permissions.
2. Install the replacement server-side key as a Fly secret; never add it to this repository, `.env.example`, or frontend JavaScript:

   ```sh
   fly secrets set STRIPE_SECRET_KEY="$STRIPE_SECRET_KEY" -a mrg
   ```

   Set `STRIPE_SECRET_KEY` in your local shell to the newly rotated key before running the command. Do not reuse the exposed key.
3. Deploy the application. The hosted Stripe Checkout session uses recurring USD prices matching the tiers above and returns to `https://mrg.fly.dev/` after success or cancellation.
4. Verify `/healthz` reports `billing_configured: true`, then click each tier and confirm the Stripe-hosted page displays the intended amount and monthly cadence before sharing the site.

The Stripe secret only enables creation of Checkout sessions. License provisioning, customer portal management, and verified webhook-based entitlement activation are not implemented by this checkout endpoint; do not treat a return to the success URL alone as proof of payment.
