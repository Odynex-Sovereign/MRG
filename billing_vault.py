"""
Odynex Axis Logistics LLC — Financial Routing Registry
Handles localized payment processing endpoints.
"""

import os

# Bank Identity Mapping: Sunrise Banks, National Association (Saint Paul, MN)
TARGET_ROUTING_ABA = "091017138"
TARGET_ACCOUNT_NUM = "692101680084"

# Safe programmatic check ensuring environment-level strings take precedence
ACTIVE_ROUTING = os.getenv("BILLING_ROUTING_NUM", TARGET_ROUTING_ABA)
ACTIVE_ACCOUNT = os.getenv("BILLING_ACCOUNT_NUM", TARGET_ACCOUNT_NUM)

def get_settlement_routing() -> dict:
    """
    Returns valid ACH infrastructure configurations for processing engines.
    """
    return {
        "vendor_name": "Odynex Axis Logistics LLC",
        "routing_number": ACTIVE_ROUTING,
        "account_number": ACTIVE_ACCOUNT,
        "clearing_method": "FedACH_Direct",
        "supported_currencies": ["USD"]
 }
