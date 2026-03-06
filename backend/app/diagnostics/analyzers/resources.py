from typing import Any, Dict, Optional


def analyze_resources(*, pod, events, current_logs: str, previous_logs: str) -> Optional[Dict[str, Any]]:
    statuses = pod.status.container_statuses or []
    for status in statuses:
        terminated = getattr(status.last_state, "terminated", None) or getattr(status.state, "terminated", None)
        if terminated and getattr(terminated, "reason", "") == "OOMKilled":
            return {
                "classification": "OOMKilled",
                "root_cause": "OOMKilled",
                "summary": "The container was terminated because it exceeded its memory limit.",
                "confidence": "high",
                "score": 98,
                "signals": {
                    "termination_reason": "OOMKilled",
                    "exit_code": getattr(terminated, "exit_code", None),
                },
                "evidence": [
                    "Last container termination reason is OOMKilled",
                    f"Last exit code is {getattr(terminated, 'exit_code', 'unknown')}",
                ],
            }

    for event in events:
        message = (getattr(event, "message", "") or "").lower()
        if "oomkilled" in message or "memory" in message and "kill" in message:
            return {
                "classification": "OOMKilled",
                "root_cause": "OOMKilled",
                "summary": "The workload shows signs of memory pressure or OOM termination.",
                "confidence": "medium",
                "score": 80,
                "signals": {"event_reason": getattr(event, "reason", "")},
                "evidence": [getattr(event, "message", "")],
            }
    return None
