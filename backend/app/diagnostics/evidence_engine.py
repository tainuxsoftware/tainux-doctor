from typing import Any, Dict, List


def build_evidence(
    result: Dict[str, Any],
    pod_name: str,
    namespace: str,
    events: list,
    current_logs: str,
    previous_logs: str,
) -> List[dict]:
    evidence = [
        {
            "source": "kubernetes",
            "message": f"Analyzed Pod/{pod_name} in namespace {namespace}",
        }
    ]

    for item in result.get("evidence", []):
        evidence.append({"source": "analyzer", "message": item})

    for event in events[:5]:
        evidence.append(
            {
                "source": "event",
                "message": f"{getattr(event, 'reason', 'Unknown')}: {getattr(event, 'message', '')}",
            }
        )

    if previous_logs:
        preview = previous_logs.strip().splitlines()[-1][:180]
        evidence.append({"source": "previous_logs", "message": preview})

    elif current_logs:
        preview = current_logs.strip().splitlines()[-1][:180]
        evidence.append({"source": "current_logs", "message": preview})

    return evidence
