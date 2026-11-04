"""Public pricing and demo checkout API."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, EmailStr, Field

from mrg.pricing import get_enterprise_modules, get_plan, get_public_plans, pricing_meta

router = APIRouter(prefix="/api", tags=["pricing"])


class CheckoutRequest(BaseModel):
    plan_id: str = Field(..., min_length=1, max_length=64)
    billing_interval: str = Field(default="month", pattern="^(month|year)$")
    email: EmailStr
    organization: str | None = Field(default=None, max_length=200)
    accept_terms: bool = False


class ContactRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    email: EmailStr
    company: str | None = Field(default=None, max_length=200)
    intent: str = Field(default="general", max_length=64)
    message: str = Field(..., min_length=10, max_length=4000)


@router.get("/pricing")
async def list_pricing() -> dict[str, Any]:
    return {
        "meta": pricing_meta(),
        "plans": get_public_plans(),
        "enterprise_modules": get_enterprise_modules(),
    }


@router.get("/pricing/{plan_id}")
async def get_pricing_plan(plan_id: str) -> dict[str, Any]:
    plan = get_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"meta": pricing_meta(), "plan": plan}


@router.post("/checkout/demo")
async def demo_checkout(body: CheckoutRequest) -> dict[str, Any]:
    """Demo checkout — does not charge a card.

    Connect Stripe by setting STRIPE_SECRET_KEY and implementing
    services/billing/checkout_engine.py; see PRICING.md and DEPLOYMENT.md.
    """
    if not body.accept_terms:
        raise HTTPException(status_code=400, detail="You must accept the terms to continue.")

    plan = get_plan(body.plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    if plan.get("contact_sales"):
        raise HTTPException(
            status_code=400,
            detail="This plan requires sales contact. Use /contact?intent=enterprise.",
        )

    amount = (
        plan.get("price_monthly") if body.billing_interval == "month" else plan.get("price_annual")
    )
    if amount is None:
        raise HTTPException(status_code=400, detail="Plan is not self-serve.")

    # Demo session id — replace with Stripe Checkout Session when live
    session_id = f"demo_cs_{body.plan_id}_{body.billing_interval}"
    return {
        "status": "demo_success",
        "message": (
            "Demo checkout completed. No payment was processed. "
            "Configure Stripe credentials to enable live subscriptions."
        ),
        "session_id": session_id,
        "plan": plan["name"],
        "plan_id": plan["id"],
        "billing_interval": body.billing_interval,
        "amount_usd": amount,
        "currency": plan.get("currency", "USD"),
        "email": str(body.email),
        "organization": body.organization,
        "trial_days": plan.get("trial_days", 0),
        "next_steps": [
            "Check your email for onboarding instructions (demo: not sent).",
            "Open /onboarding to explore the product tour.",
            "See PRICING.md to connect Stripe for production charges.",
        ],
    }


@router.post("/contact")
async def contact_sales(body: ContactRequest) -> dict[str, Any]:
    """Capture enterprise / support inquiries (stored as log in production; demo returns ack)."""
    return {
        "status": "received",
        "message": "Thanks — our team will respond within one business day (demo acknowledgment).",
        "intent": body.intent,
        "reference": f"inq_{body.intent}_{abs(hash(body.email)) % 10_000_000}",
    }


@router.get("/metrics/demo")
async def metrics_demo() -> dict[str, Any]:
    """Sample metrics for the /metrics dashboard. Clearly labeled as demo data."""
    return {
        "label": "DEMO DATA — not live production metrics",
        "period": "last_30_days",
        "acquisition": {
            "visitors": 12400,
            "signups": 860,
            "visitor_to_signup_rate": 0.069,
        },
        "activation": {
            "activated_users": 520,
            "signup_to_activation_rate": 0.605,
        },
        "revenue": {
            "mrr_usd": 42800,
            "arr_usd": 513600,
            "trial_to_paid_rate": 0.18,
            "arpu_usd": 82,
        },
        "retention": {
            "logo_churn_monthly": 0.035,
            "net_revenue_retention": 1.08,
            "ltv_usd_estimate": 2100,
        },
        "funnel": [
            {"step": "Landing", "count": 12400},
            {"step": "Pricing viewed", "count": 4100},
            {"step": "Checkout started", "count": 980},
            {"step": "Trial started", "count": 860},
            {"step": "Activated", "count": 520},
            {"step": "Paid", "count": 155},
        ],
        "subscriptions": {
            "active": 412,
            "trialing": 94,
            "canceled_30d": 18,
            "past_due": 7,
        },
    }


@router.get("/admin/summary")
async def admin_summary(token: str | None = Query(default=None)) -> dict[str, Any]:
    """Lightweight admin summary. Protect with ADMIN_API_TOKEN in production."""
    from mrg.config import get_settings

    settings = get_settings()
    expected = getattr(settings, "admin_api_token", None) or None
    # Always allow in non-production when token unset; require match when set
    if settings.is_production and expected and token != expected:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return {
        "users_total": 1280,
        "subscriptions_active": 412,
        "open_support_tickets": 6,
        "feature_flags": {
            "enable_billing": settings.enable_billing,
            "enable_sensory": settings.enable_sensory,
            "sandbox_mode": not settings.has_deepseek,
        },
        "plans": [{"id": p["id"], "name": p["name"]} for p in get_public_plans()],
        "note": "Demo aggregates — connect database and Stripe for live admin data.",
    }
