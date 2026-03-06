from typing import Any, Dict, Optional


def analyze_scheduling(*, pod, events, current_logs: str, previous_logs: str) -> Optional[Dict[str, Any]]:
    if getattr(pod.status, "phase", "") != "Pending":
        return None

    for event in events:
        reason = getattr(event, "reason", "")
        message = getattr(event, "message", "")
        if reason == "FailedScheduling":
            return {
                "classification": "Pending",
                "root_cause": "FailedScheduling",
                "summary": "The pod is Pending because the scheduler could not place it on any available node.",
                "confidence": "high",
                "score": 92,
                "signals": {"phase": "Pending", "event_reason": reason},
                "evidence": [message or "Scheduler reported FailedScheduling"],
            }

    return {
        "classification": "Pending",
        "root_cause": "Pod Pending",
        "summary": "The pod is still Pending and may be waiting for scheduling or dependencies such as PVCs.",
        "confidence": "medium",
        "score": 60,
        "signals": {"phase": "Pending"},
        "evidence": ["Pod phase is Pending"],
    }
