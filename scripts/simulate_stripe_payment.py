import sys
import os
import time
import requests
import hmac
import hashlib

def trigger_mock_webhook(tenant_id: str, tier: str):
    """
    Generates a cryptographically sound signature payload to test 
    your asynchronous /api/v1/billing/webhook router layout locally.
    """
    url = "http://localhost:8000/api/v1/billing/webhook"
    secret = "whsec_placeholder"
    
    timestamp = str(int(time.time()))
    mock_payload = f"""{{
        "id": "evt_test_{timestamp}",
        "type": "checkout.session.completed",
        "data": {{
            "object": {{
                "id": "cs_test_url_token",
                "metadata": {{
                    "tenant_id": "{tenant_id}",
                    "tier_selection": "{tier}"
                }}
            }}
        }}
    }}"""

    # Generate standard cryptographic signature matching Stripe protocols
    signed_payload = f"t={timestamp},v1={hmac.new(secret.encode(), f'{timestamp}.{mock_payload}'.encode(), hashlib.sha256).hexdigest()}"
    headers = {
        "stripe-signature": signed_payload,
        "Content-Type": "application/json"
    }

    print(f"[*] Dispatched webhook pulse for tenant '{tenant_id}' [{tier.upper()}]...")
    response = requests.post(url, data=mock_payload, headers=headers)
    print(f"[+] Server Response Block ({response.status_code}): {response.json()}")

if __name__ == "__main__":
    trigger_mock_webhook(tenant_id="sandbox_default_user", tier="enterprise")
