# Metrics & analytics

## Event names (client)

| Event | When |
|-------|------|
| `page_view` | Every page load (`app/assets/app.js`) |
| `cta_click` | Primary CTAs |
| `select_plan` | Pricing card selection |
| `checkout_view` | Checkout page |
| `checkout_demo_success` | Demo checkout completed |
| `checkout_error` | Checkout failure |
| `onboarding_view` | Onboarding |
| `contact_submit` | Contact form |
| `demo_ws_open` | Demo WebSocket connected |

Wire `window.MRG_ANALYTICS = { track(event, props) { … } }` to Segment, PostHog, or similar. No third-party SDK is bundled by default (privacy-conscious).

## Server-side funnel metrics

Documented in `/api/metrics/demo` response schema: visitors, signups, activation, MRR/ARR, churn, NRR, LTV estimate, subscription states.

Replace demo provider with warehouse queries when billing and auth are live.
