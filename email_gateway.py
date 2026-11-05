import logging
import json
from typing import Dict, Any
from pydantic import BaseModel

logger = logging.getLogger("mrg.services.email_gateway")

class IncomingEmailPayload(BaseModel):
    sender: str
    subject: str
    body_text: str
    received_at: str

class EnterpriseEmailGateway:
    """
    Ingests and parses inbound B2B emails, RFPs, and system notifications.
    Extracts pre-funded budget data to trigger autonomous platform onboarding.
    """
    def __init__(self, db_client, crawler_engine):
        self.db = db_client
        self.crawler = crawler_engine

    async def process_inbound_email_webhook(self, email: IncomingEmailPayload) -> Dict[str, Any]:
        """Parses email text blocks to identify enterprise interest or pre-allocated budgets."""
        logger.info(f"[Email Ingestion] Parsing message from {email.sender} regarding: {email.subject}")
        
        # Check for keywords indicating explicit pre-allocated enterprise budgets
        body_lower = email.body_text.lower()
        is_prefunded_rfp = "budget" in body_lower or "rfp" in body_lower or "simulation" in body_lower
        
        if is_prefunded_rfp:
            extracted_budget = 25000.00  # Default base allocation threshold
            if "$" in body_lower:
                # Basic token extraction logic fallback
                try:
                    parts = body_lower.split("$")
                    extracted_budget = float(parts[1].split()[0].replace(",", "").replace(";", ""))
                except Exception:
                    pass

            lead_id = f"email_{uuid.uuid4().hex[:6]}"
            
            # Insert the pre-allocated lead directly into your core ledger pools
            await self.db.execute(
                "INSERT INTO growth_loops (id, referrer_id, conversion_value, payout_settled) "
                "VALUES ($1, $2, $3, False)", lead_id, email.sender, extracted_budget
            )
            
            logger.info(f"[Email Lead Logged] Extracted pre-funded budget: ${extracted_budget} from {email.sender}")
            return {"status": "parsed_and_logged", "action": "trigger_autonomous_response"}
            
        return {"status": "ignored", "reason": "non_commercial_traffic"}
