import httpx
import logging
from typing import Dict, Any, Optional
from app.config import settings

logger = logging.getLogger("mrg.services.social_webhook")

class CrisisCommunicationsOrchestrator:
    """
    Handles out-of-band infrastructure routing during high-pressure simulation events.
    Bypasses compromised channels using Twilio (SMS/Voice) and dedicated platform webhooks.
    """
    def __init__(self):
        # Gracefully falls back to sandbox/mock mode if keys are missing from fly secrets
        self.twilio_account_sid: Optional[str] = getattr(settings, "TWILIO_ACCOUNT_SID", None)
        self.twilio_auth_token: Optional[str] = getattr(settings, "TWILIO_AUTH_TOKEN", None)
        self.twilio_from_number: Optional[str] = getattr(settings, "TWILIO_FROM_NUMBER", None)
        self.enterprise_webhook_url: Optional[str] = getattr(settings, "ENTERPRISE_WEBHOOK_URL", None)

    async def broadcast_crisis_event(self, event_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entrypoint to broadcast an explosive scenario modification across all channels.
        """
        sector = event_payload.get("sector", "GLOBAL_MACRO")
        severity = event_payload.get("severity", "CRITICAL")
        message = event_payload.get("message", "A planet-scale structural breakdown has been detected.")
        executive_contacts = event_payload.get("target_phones", [])

        results = {"sms_dispatched": 0, "webhook_delivered": False}

        # 1. Dispatch Out-of-Band Text Alerts via Twilio
        if self.twilio_account_sid and self.twilio_auth_token and executive_contacts:
            sms_text = f"🚨 [MRG CRISIS GRID] {severity} ALERT | Sector: {sector} \n\n{message}\n\nAction Required: Secure communication lines immediately."
            for phone in executive_contacts:
                success = await self._send_twilio_sms(phone, sms_text)
                if success:
                    results["sms_dispatched"] += 1
        else:
            logger.warning("[MRG] Twilio credentials missing or phone list empty. Skipping Out-of-Band SMS.")

        # 2. Dispatch Live War-Room Feeds (Slack/Teams JSON schema format)
        if self.enterprise_webhook_url:
            webhook_payload = {
                "text": f"⚠️ *MRG Simulation Alert - Structural Failure Induced* ⚠️",
                "attachments": [{
                    "color": "#FF0000" if severity == "CRITICAL" else "#FFA500",
                    "fields": [
                        {"title": "Simulation Sector", "value": sector, "short": True},
                        {"title": "Stress Severity Level", "value": severity, "short": True},
                        {"title": "Operational Vector", "value": message, "short": False}
                    ],
                    "footer": "MRG Executive Crisis Grid Engine",
                }]
            }
            results["webhook_delivered"] = await self._send_enterprise_webhook(webhook_payload)
        else:
            logger.warning("[MRG] Enterprise Webhook URL missing. Skipping workspace notification.")

        return results

    async def _send_twilio_sms(self, to_phone: str, body: str) -> bool:
        """Executes secure HTTPS POST to the Twilio Messages API endpoint."""
        url = f"https://twilio.com{self.twilio_account_sid}/Messages.json"
        auth = (self.twilio_account_sid, self.twilio_auth_token)
        data = {
            "To": to_phone,
            "From": self.twilio_from_number,
            "Body": body
        }
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(url, auth=auth, data=data)
                if response.status_code == 201:
                    logger.info(f"[MRG SMS] Successfully alerted contact: {to_phone}")
                    return True
                else:
                    logger.error(f"[MRG SMS Failed] Twilio responded with status: {response.status_code} | {response.text}")
                    return False
        except Exception as e:
            logger.error(f"[MRG SMS Exception] Failed to transmit via Twilio layer: {str(e)}")
            return False

    async def _send_enterprise_webhook(self, payload: Dict[str, Any]) -> bool:
        """Forwards formatted card payloads directly to Teams or Slack channels."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(self.enterprise_webhook_url, json=payload)
                if response.status_code in:
                    logger.info("[MRG Webhook] Dispatched war room payload successfully.")
                    return True
                else:
                    logger.error(f"[MRG Webhook Failed] Endpoint rejected payload: {response.status_code}")
                    return False
        except Exception as e:
            logger.error(f"[MRG Webhook Exception] Failed connection to communications layout: {str(e)}")
            return False
