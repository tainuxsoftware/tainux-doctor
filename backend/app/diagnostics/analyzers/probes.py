from typing import Any, Dict, Optional


def analyze_probes(*, pod, events, current_logs: str, previous_logs: str) -> Optional[Dict[str, Any]]:
    for event in events:
        message = getattr(event, "message", "") or ""
        lowered = message.lower()
        if "readiness probe failed" in lowered or "liveness probe failed" in lowered or "startup probe failed" in lowered:
            return {
                "classification": "ProbeFailure",
                "root_cause": "Probe failure",
                "summary": "The container is failing one or more health probes.",
                "confidence": "high",
                "score": 85,
                "signals": {"probe_message": message},
                "evidence": [message],
            }
    return None
