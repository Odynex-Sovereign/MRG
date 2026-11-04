# MRG Headless API Integration Matrix
### Developer Token Authentication & High-Frequency Streaming Specifications

The MRG simulation engine exposes an unbundled, headless telemetry pipeline allowing enterprise risk dashboards to consume raw crisis data frames without browser frontends.

---

## 🔒 1. Authentication Lifecycle
All inbound HTTP data queries must pass a cryptographic developer token inside your transaction headers. 

1. Funded developer keys are generated inside your corporate portal dashboard.
2. Tokens utilize the standard format prefix: `mrg_live_sk_...`
3. Pre-fund your billing wallet via Stripe or PayPal/Venmo Braintree to activate your key limits.

### Outbound Connection Header Format
```http
GET /api/marketplace/consume-api-telemetry HTTP/1.1
Host: mrg.fly.dev
Authorization: Bearer mrg_live_sk_your_secret_token_here
Content-Type: application/json
```

---

## 🛰️ 2. Core Telemetry Endpoints

### Ingest Live Non-Persisted Data Frame
* **Endpoint:** `POST https://fly.dev`
* **Method:** `POST`
* **Payload Structure:**
```json
{
  "developer_secret_key": "mrg_live_sk_your_secret_token_here",
  "data_packets_processed": 250
}
```

### Inbound Server Response (Status: 200 OK)
```json
{
  "status": "debited",
  "amount_charged": 0.1000,
  "remaining_ledger_balance_usd": 1450.45,
  "execution_telemetry": {
    "compute_topology": "parallel_tensor_grid",
    "measured_processing_throughput_tflops": 245.2
  }
}
```

---

## 💰 3. Wholesale API Tariffs & Rates
* **Base Wholesale Rate:** $0.0004 USD per data packet frame processed.
* **Auto-Throttling:** Connections are automatically rate-limited if your pre-funded `billing_vault` ledger balance drops below$5.00 USD.
