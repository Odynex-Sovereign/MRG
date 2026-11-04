# services/marketing/growth_loops.py
import os
import hashlib
from typing import Dict, Any

BASE_APP_URL = os.getenv("APP_BASE_URL", "https://fly.dev")

class ViralGrowthEngine:
    """
    Implements a Product-Led Growth (PLG) loop.
    Turns client crisis simulation data into an auto-marketing asset.
    """
    
    @staticmethod
    def generate_viral_scorecard(session_id: str, composure_score: float, vertical: str) -> Dict[str, Any]:
        """
        Creates an interactive crisis link for an executive to share with peers.
        Acts as an organic acquisition loop for net-new software sign-ups.
        """
        # Generate an absolute signature for defense/integrity confirmation
        payload_hash = hashlib.sha256(f"{session_id}-{composure_score}".encode()).hexdigest()[:8]
        
        # Build self-marketing textual summaries based on performance benchmarks
        share_text = f"I just maintained a {composure_score}% composure index running the {vertical} macro-crisis simulation matrix. Can your executive suite beat this response velocity?"
        referral_link = f"{BASE_APP_URL}/challenge/{session_id}?ref={payload_hash}&v={vertical}"
        
        return {
            "share_text": share_text,
            "embedded_url": referral_link,
            "social_payloads": {
                "linkedin": f"https://linkedin.com{referral_link}",
                "twitter_x": f"https://twitter.com{share_text}&url={referral_link}"
            }
        }
import asyncio  # <-- Paste this line right at the very top
from fastapi import FastAPI
from services.growth_loops import AutomatedMonetizationEngine
# ... keep your other existing imports exactly as they are below this
