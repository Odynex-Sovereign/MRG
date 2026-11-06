"""
Central pricing configuration.

All public prices and entitlements live here.
Override monthly/annual amounts via environment variables if needed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PlanEntitlements:
    max_simulations_per_month: int | None  # None = unlimited
    max_team_members: int
    black_swan_challenges: bool
    digital_twin_feedback: bool
    export_reports: bool
    api_access: bool
    priority_support: bool
    sso: bool
    audit_logs: bool
    dedicated_deployment: bool
    custom_scenarios: bool


@dataclass
class Plan:
    id: str
    name: str
    description: str
    monthly_usd: float
    annual_usd: float  # billed yearly (usually ~2 months free)
    currency: str = "USD"
    popular: bool = False
    trial_days: int = 0
    entitlements: PlanEntitlements = field(default_factory=lambda: PlanEntitlements(
        max_simulations_per_month=5,
        max_team_members=1,
        black_swan_challenges=False,
        digital_twin_feedback=False,
        export_reports=False,
        api_access=False,
        priority_support=False,
        sso=False,
        audit_logs=False,
        dedicated_deployment=False,
        custom_scenarios=False,
    ))
    features: list[str] = field(default_factory=list)
    cta: str = "Get started"
    audience: str = "individuals"


# ---------------------------------------------------------------------------
# Canonical public plans — adjustable via env or admin later
# ---------------------------------------------------------------------------

PLANS: dict[str, Plan] = {
    "free": Plan(
        id="free",
        name="Free",
        description="Essential personal practice. No credit card required.",
        monthly_usd=0,
        annual_usd=0,
        trial_days=0,
        audience="individuals",
        features=[
            "3 simulations per month",
            "Basic composure feedback",
            "Community scenarios",
            "Mobile + desktop access",
        ],
        entitlements=PlanEntitlements(
            max_simulations_per_month=3,
            max_team_members=1,
            black_swan_challenges=False,
            digital_twin_feedback=False,
            export_reports=False,
            api_access=False,
            priority_support=False,
            sso=False,
            audit_logs=False,
            dedicated_deployment=False,
            custom_scenarios=False,
        ),
        cta="Start free",
    ),
    "personal": Plan(
        id="personal",
        name="Personal",
        description="For daily users who want deeper practice and higher limits.",
        monthly_usd=5,
        annual_usd=50,
        popular=True,
        trial_days=14,
        audience="individuals",
        features=[
            "30 simulations per month",
            "Black Swan Challenge access",
            "Digital-twin composure scoring",
            "Exportable session reports",
            "Email support",
        ],
        entitlements=PlanEntitlements(
            max_simulations_per_month=30,
            max_team_members=1,
            black_swan_challenges=True,
            digital_twin_feedback=True,
            export_reports=True,
            api_access=False,
            priority_support=False,
            sso=False,
            audit_logs=False,
            dedicated_deployment=False,
            custom_scenarios=False,
        ),
        cta="Start 14-day trial",
    ),
    "household": Plan(
        id="household",
        name="Household / Family",
        description="Shared workspace for up to 5 people with privacy controls.",
        monthly_usd=10,
        annual_usd=100,
        trial_days=14,
        audience="families",
        features=[
            "Everything in Personal",
            "Up to 5 members",
            "Shared scenario library",
            "Individual privacy controls",
            "Family progress overview",
        ],
        entitlements=PlanEntitlements(
            max_simulations_per_month=80,
            max_team_members=5,
            black_swan_challenges=True,
            digital_twin_feedback=True,
            export_reports=True,
            api_access=False,
            priority_support=False,
            sso=False,
            audit_logs=False,
            dedicated_deployment=False,
            custom_scenarios=False,
        ),
        cta="Start 14-day trial",
    ),
    "pro": Plan(
        id="pro",
        name="Pro",
        description="Advanced workflows, higher limits, and integrations for power users.",
        monthly_usd=15,
        annual_usd=150,
        trial_days=14,
        audience="professionals",
        features=[
            "Unlimited simulations",
            "Custom scenario builder",
            "API access (read)",
            "Priority email support",
            "Advanced analytics",
            "Export to PDF / CSV",
        ],
        entitlements=PlanEntitlements(
            max_simulations_per_month=None,
            max_team_members=1,
            black_swan_challenges=True,
            digital_twin_feedback=True,
            export_reports=True,
            api_access=True,
            priority_support=True,
            sso=False,
            audit_logs=False,
            dedicated_deployment=False,
            custom_scenarios=True,
        ),
        cta="Start 14-day trial",
    ),
    "team": Plan(
        id="team",
        name="Team",
        description="Central billing, collaboration, and basic administration.",
        monthly_usd=10,  # per user / month
        annual_usd=8,    # per user / month when billed annually
        trial_days=14,
        audience="teams",
        features=[
            "Everything in Pro",
            "Per-seat billing",
            "Shared workspaces",
            "Basic role management",
            "Team analytics",
            "Priority support",
        ],
        entitlements=PlanEntitlements(
            max_simulations_per_month=None,
            max_team_members=50,
            black_swan_challenges=True,
            digital_twin_feedback=True,
            export_reports=True,
            api_access=True,
            priority_support=True,
            sso=False,
            audit_logs=True,
            dedicated_deployment=False,
            custom_scenarios=True,
        ),
        cta="Start team trial",
    ),
    "nonprofit": Plan(
        id="nonprofit",
        name="Nonprofit / Education",
        description="40–60% discount for verified nonprofits, schools, and universities.",
        monthly_usd=0,  # custom after verification
        annual_usd=0,
        audience="institutions",
        features=[
            "Discounted Team or Pro rates",
            "Eligibility verification workflow",
            "Shared institutional library",
            "Training resources",
        ],
        entitlements=PlanEntitlements(
            max_simulations_per_month=None,
            max_team_members=100,
            black_swan_challenges=True,
            digital_twin_feedback=True,
            export_reports=True,
            api_access=True,
            priority_support=True,
            sso=False,
            audit_logs=True,
            dedicated_deployment=False,
            custom_scenarios=True,
        ),
        cta="Request eligibility",
    ),
    "enterprise": Plan(
        id="enterprise",
        name="Enterprise / Government",
        description="Custom quote — SSO, audit logs, dedicated options, SLA.",
        monthly_usd=0,
        annual_usd=0,
        audience="institutions",
        features=[
            "SSO / SAML / OIDC (when configured)",
            "Advanced admin & audit logs",
            "Dedicated or private deployment",
            "Custom scenarios & training",
            "SLA & onboarding support",
            "Institutional buy-out path",
        ],
        entitlements=PlanEntitlements(
            max_simulations_per_month=None,
            max_team_members=10_000,
            black_swan_challenges=True,
            digital_twin_feedback=True,
            export_reports=True,
            api_access=True,
            priority_support=True,
            sso=True,
            audit_logs=True,
            dedicated_deployment=True,
            custom_scenarios=True,
        ),
        cta="Contact sales",
    ),
}


# Institutional buy-out guidance (illustrative only)
INSTITUTIONAL_RANGES = {
    "small": {
        "label": "Small nonprofit, school, or municipality",
        "range_usd": "15,000 – 40,000",
        "notes": "Typical perpetual license or multi-year SaaS for limited user counts.",
    },
    "mid": {
        "label": "Mid-size municipality, university department, or regional organization",
        "range_usd": "40,000 – 125,000",
        "notes": "Includes setup, training, and defined support years.",
    },
    "large": {
        "label": "Enterprise, university-wide, state-level, or regulated deployment",
        "range_usd": "125,000 – 500,000+",
        "notes": "Custom scope; often includes dedicated deployment and compliance support.",
    },
}


def get_plan(plan_id: str) -> Plan | None:
    return PLANS.get(plan_id)


def list_public_plans() -> list[dict[str, Any]]:
    """Serialize plans for API and UI (no internal secrets)."""
    result = []
    for p in PLANS.values():
        result.append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "monthly_usd": p.monthly_usd,
            "annual_usd": p.annual_usd,
            "currency": p.currency,
            "popular": p.popular,
            "trial_days": p.trial_days,
            "features": p.features,
            "cta": p.cta,
            "audience": p.audience,
            "entitlements": {
                "max_simulations_per_month": p.entitlements.max_simulations_per_month,
                "max_team_members": p.entitlements.max_team_members,
                "black_swan_challenges": p.entitlements.black_swan_challenges,
                "digital_twin_feedback": p.entitlements.digital_twin_feedback,
                "export_reports": p.entitlements.export_reports,
                "api_access": p.entitlements.api_access,
                "priority_support": p.entitlements.priority_support,
                "sso": p.entitlements.sso,
                "audit_logs": p.entitlements.audit_logs,
                "dedicated_deployment": p.entitlements.dedicated_deployment,
                "custom_scenarios": p.entitlements.custom_scenarios,
            },
        })
    return result


def plan_allows(plan_id: str, feature: str) -> bool:
    plan = get_plan(plan_id)
    if not plan:
        return False
    return bool(getattr(plan.entitlements, feature, False))
