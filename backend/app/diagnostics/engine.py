from typing import Any, Dict, List, Optional

from app.collectors.kubernetes.client import get_core_v1_api
from app.collectors.kubernetes.events import get_related_events
from app.collectors.kubernetes.logs import get_pod_logs
from app.collectors.kubernetes.pods import find_problem_pod, get_pod
from app.core.config import settings
from app.core.exceptions import DiagnosisError
from app.diagnostics.analyzers.image_pull import analyze_image_pull
from app.diagnostics.analyzers.pod_crash import analyze_pod_crash
from app.diagnostics.analyzers.probes import analyze_probes
from app.diagnostics.analyzers.resources import analyze_resources
from app.diagnostics.analyzers.scheduling import analyze_scheduling
from app.diagnostics.evidence_engine import build_evidence
from app.diagnostics.recommendation_engine import build_recommendations


def _assert_namespace_allowed(namespace: str) -> None:
    allowed = settings.allowed_namespaces_list
    if allowed and namespace not in allowed:
        raise DiagnosisError(f"namespace '{namespace}' is not allowed by configuration")


def _select_pod_name(question: str, namespace: str, explicit_name: Optional[str]) -> str:
    if explicit_name:
        return explicit_name
    api = get_core_v1_api()
    pod_name = find_problem_pod(api, namespace)
    if not pod_name:
        raise DiagnosisError(f"no pods found in namespace '{namespace}'")
    return pod_name


def run_diagnosis(
    question: str,
    namespace: Optional[str] = None,
    resource_name: Optional[str] = None,
    include_logs: bool = True,
) -> Dict[str, Any]:
    target_namespace = namespace or settings.default_namespace
    _assert_namespace_allowed(target_namespace)

    api = get_core_v1_api()
    pod_name = _select_pod_name(question, target_namespace, resource_name)
    pod = get_pod(api, target_namespace, pod_name)
    events = get_related_events(api, target_namespace, pod_name)
    current_logs = get_pod_logs(api, target_namespace, pod_name, previous=False) if include_logs else ""
    previous_logs = get_pod_logs(api, target_namespace, pod_name, previous=True) if include_logs else ""

    analyses: List[Dict[str, Any]] = []
    for analyzer in (
        analyze_pod_crash,
        analyze_image_pull,
        analyze_scheduling,
        analyze_probes,
        analyze_resources,
    ):
        result = analyzer(pod=pod, events=events, current_logs=current_logs, previous_logs=previous_logs)
        if result:
            analyses.append(result)

    if analyses:
        winner = sorted(analyses, key=lambda item: item.get("score", 0), reverse=True)[0]
    else:
        winner = {
            "root_cause": "Unknown root cause, more evidence required",
            "summary": "The pod appears unhealthy, but no specific root cause was confidently detected.",
            "confidence": "low",
            "signals": {
                "phase": getattr(pod.status, "phase", "Unknown"),
                "restart_count": sum((s.restart_count for s in (pod.status.container_statuses or [])), 0),
            },
        }

    evidence = build_evidence(winner, pod_name, target_namespace, events, current_logs, previous_logs)
    recommendations = build_recommendations(winner)

    return {
        "summary": winner["summary"],
        "affected_resource": f"Pod/{pod_name} in namespace {target_namespace}",
        "root_cause": winner["root_cause"],
        "confidence": winner["confidence"],
        "evidence": evidence,
        "recommendations": recommendations,
        "raw_signals": winner.get("signals", {}),
    }
