from typing import Any, Dict, Optional


def analyze_pod_crash(*, pod, events, current_logs: str, previous_logs: str) -> Optional[Dict[str, Any]]:
    statuses = pod.status.container_statuses or []
    for status in statuses:
        waiting = getattr(status.state, "waiting", None)
        terminated = getattr(status.last_state, "terminated", None) or getattr(status.state, "terminated", None)

        if waiting and getattr(waiting, "reason", "") == "CrashLoopBackOff":
            return {
                "classification": "CrashLoopBackOff",
                "root_cause": "CrashLoopBackOff",
                "summary": "The pod is repeatedly crashing during startup or shortly after becoming ready.",
                "confidence": "high",
                "score": 90,
                "signals": {
                    "waiting_reason": waiting.reason,
                    "restart_count": status.restart_count,
                },
                "evidence": [
                    f"Container is in waiting state with reason {waiting.reason}",
                    f"Restart count is {status.restart_count}",
                ],
            }

        if terminated and getattr(terminated, "reason", "") == "Error":
            return {
                "classification": "CrashLoopBackOff",
                "root_cause": "Container terminated with Error",
                "summary": "The container terminated with a generic error and appears to be restarting repeatedly.",
                "confidence": "medium",
                "score": 75,
                "signals": {
                    "termination_reason": terminated.reason,
                    "exit_code": getattr(terminated, "exit_code", None),
                },
                "evidence": [
                    f"Last termination reason is {terminated.reason}",
                    f"Last exit code is {getattr(terminated, 'exit_code', 'unknown')}",
                ],
            }
    return None
