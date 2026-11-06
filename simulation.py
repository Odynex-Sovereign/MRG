"""
Sandbox crisis / composure simulation engine.

All outputs are clearly labeled as simulated. No external model calls occur
unless API keys are configured and the caller opts in.
"""

from __future__ import annotations

import asyncio
import random
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, AsyncIterator


@dataclass
class SimulationSession:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    started_at: float = field(default_factory=time.time)
    events_emitted: int = 0


SCENARIOS = {
    "black_swan_supply": {
        "title": "Supply Chain Black Swan",
        "description": "A rare multi-region logistics disruption forces rapid prioritization decisions.",
        "steps": [
            "Initial disruption reports arrive from two continents.",
            "Key supplier goes offline; secondary routes congested.",
            "Media and stakeholder pressure increase.",
            "You must choose prioritization: critical health supplies vs commercial contracts.",
            "Debrief: decision rationale and composure metrics.",
        ],
    },
    "cyber_cascade": {
        "title": "Cascading Cyber Event",
        "description": "A targeted outage spreads across partner systems. Practice calm triage.",
        "steps": [
            "Primary identity provider latency spikes.",
            "Secondary payment gateway timeouts reported.",
            "Customer support volume triples.",
            "Choose containment vs transparency messaging.",
            "Debrief: communication clarity and stress indicators.",
        ],
    },
    "macro_shock": {
        "title": "Macro Policy Shock",
        "description": "Sudden regulatory and market shifts require coordinated response.",
        "steps": [
            "Overnight policy announcement affects three operating regions.",
            "Currency and logistics costs move sharply.",
            "Board requests an options brief within the hour.",
            "Select near-term actions and communication plan.",
            "Debrief: decisiveness under incomplete information.",
        ],
    },
}


def _compose_score() -> dict[str, Any]:
    """Generate realistic-looking but clearly simulated composure metrics."""
    base = random.randint(68, 94)
    return {
        "composure_score": base,
        "vocal_stress_index": max(10, 100 - base + random.randint(-8, 12)),
        "tactical_decisiveness": min(99, base + random.randint(-5, 10)),
        "systemic_risk_mitigation": min(99, base + random.randint(-8, 8)),
        "label": "SIMULATED",
    }


async def run_sandbox_simulation(
    session: SimulationSession,
    scenario_id: str = "black_swan_supply",
) -> AsyncIterator[dict[str, Any]]:
    scenario = SCENARIOS.get(scenario_id) or SCENARIOS["black_swan_supply"]
    yield {
        "type": "scenario_start",
        "session_id": session.id,
        "scenario": scenario_id,
        "title": scenario["title"],
        "description": scenario["description"],
        "note": "This is a sandbox simulation. Metrics are illustrative.",
    }
    await asyncio.sleep(0.4)

    for i, step in enumerate(scenario["steps"], start=1):
        session.events_emitted += 1
        yield {
            "type": "step",
            "index": i,
            "total": len(scenario["steps"]),
            "text": step,
            "timestamp": time.time(),
        }
        await asyncio.sleep(0.6 + random.random() * 0.4)

        if i == len(scenario["steps"]) // 2:
            yield {
                "type": "metrics_update",
                "metrics": _compose_score(),
            }

    final = _compose_score()
    yield {
        "type": "scenario_complete",
        "session_id": session.id,
        "metrics": final,
        "debrief": (
            "Practice complete. Review your decision points and emotional regulation. "
            "In a live session with configured models, richer digital-twin feedback would appear here."
        ),
        "note": "All scores are simulated for demonstration.",
    }
