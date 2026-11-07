import os
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Odynex_Social_Pipeline")

class SocialAutomationHook:
    def __init__(self):
        self.webhook_url = os.getenv("SOCIAL_AUTOMATION_WEBHOOK_URL")
        self.platform_domain = "https://fly.dev"

    async def broadcast_failed_challenge(self, user_name: str, headline: str, score: int, vertical: str) -> bool:
        """
        Dispatches a high-impact social roast snippet to drive traction back to the platform.
        """
        if not self.webhook_url:
            logger.warning("SOCIAL_AUTOMATION_WEBHOOK_URL not set. Suppressing viral broadcast loop.")
            return False

        # Construct a viral, attention-grabbing engagement payload based on the sector context
        social_text = (
            f"🚨 BLACK SWAN SYSTEM CRITICAL 🚨\n\n"
            f"User '{user_name}' just ran the high-stakes '{vertical}' Crucible on the Odynex Grid.\n\n"
            f"📉 SYSTEM FAILURE: {headline}\n"
            f"📊 Final Composure Rating: {score}/100\n\n"
            f"Think you can protect the transpacific logistics corridor better under pressure? "
            f"Accept the challenge here: {self.platform_domain}/challenge"
        )

        payload = {
            "text": social_text,
            "meta": {
                "engine_architecture": "ODYNEX_AXIS_LOGISTICS",
                "legal_framework_compliance": "TUTSA_WTO_COMPLIANT"
            }
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.webhook_url, json=payload, timeout=5.0)
                if response.status_code == 200:
                    logger.info(f"Successfully broadcasted viral alert for user: {user_name}")
                    return True
                logger.error(f"Social webhook responded with error status: {response.status_code}")
                return False
            except Exception as e:
                logger.error(f"Failed to reach social automation webhook grid: {e}")
                return False
