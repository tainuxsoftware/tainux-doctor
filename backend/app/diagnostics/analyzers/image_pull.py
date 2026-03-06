from typing import Any, Dict, Optional


def analyze_image_pull(*, pod, events, current_logs: str, previous_logs: str) -> Optional[Dict[str, Any]]:
    statuses = pod.status.container_statuses or []
    for status in statuses:
        waiting = getattr(status.state, "waiting", None)
        reason = getattr(waiting, "reason", "") if waiting else ""
        if reason in {"ImagePullBackOff", "ErrImagePull"}:
            return {
                "classification": "ImagePullBackOff",
                "root_cause": reason,
                "summary": "The pod cannot pull its container image from the configured registry.",
                "confidence": "high",
                "score": 95,
                "signals": {"waiting_reason": reason},
                "evidence": [f"Container waiting reason is {reason}"],
            }

    for event in events:
        msg = (getattr(event, "message", "") or "").lower()
        if "failed to pull image" in msg or "pull access denied" in msg:
            return {
                "classification": "ImagePullBackOff",
                "root_cause": "Image pull failure",
                "summary": "The pod cannot retrieve its image because the registry pull failed.",
                "confidence": "high",
                "score": 88,
                "signals": {"event_reason": getattr(event, "reason", "")},
                "evidence": [getattr(event, "message", "")],
            }
    return None
