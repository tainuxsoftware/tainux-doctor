from typing import Any, Dict, List

_MAP = {
    "OOMKilled": [
        {
            "action": "Increase container memory limit",
            "rationale": "The container likely exceeded its configured memory limit."
        },
        {
            "action": "Review startup and steady-state memory usage",
            "rationale": "Application memory spikes often trigger OOMKilled restarts."
        },
    ],
    "ImagePullBackOff": [
        {
            "action": "Validate the image name and tag",
            "rationale": "Registry or tag errors commonly cause pull failures."
        },
        {
            "action": "Check image pull secret permissions",
            "rationale": "Private registry authentication may be missing or invalid."
        },
    ],
    "Pending": [
        {
            "action": "Review scheduler events and node capacity",
            "rationale": "Pods remain Pending when the scheduler cannot place them."
        },
        {
            "action": "Inspect requests, limits, taints and tolerations",
            "rationale": "Scheduling constraints often block pod placement."
        },
    ],
    "ProbeFailure": [
        {
            "action": "Validate readiness and liveness probe configuration",
            "rationale": "Incorrect path, port or timing causes repeated probe failures."
        }
    ],
    "CrashLoopBackOff": [
        {
            "action": "Inspect application logs and last termination reason",
            "rationale": "CrashLoopBackOff usually indicates repeated startup failure."
        }
    ],
}


def build_recommendations(result: Dict[str, Any]) -> List[dict]:
    cause = result.get("classification", "")
    return _MAP.get(cause, [{
        "action": "Collect more runtime evidence",
        "rationale": "No strong classification was found from the current signals."
    }])
