from typing import Optional
from kubernetes.client import CoreV1Api


def get_pod(api: CoreV1Api, namespace: str, pod_name: str):
    return api.read_namespaced_pod(name=pod_name, namespace=namespace)


def list_pods(api: CoreV1Api, namespace: str):
    return api.list_namespaced_pod(namespace=namespace).items


def find_problem_pod(api: CoreV1Api, namespace: str) -> Optional[str]:
    pods = list_pods(api, namespace)
    for pod in pods:
        statuses = pod.status.container_statuses or []
        if pod.status.phase not in {"Running", "Succeeded"}:
            return pod.metadata.name
        for status in statuses:
            waiting = getattr(status.state, "waiting", None)
            terminated = getattr(status.state, "terminated", None)
            if waiting or terminated or status.restart_count > 0:
                return pod.metadata.name
    return pods[0].metadata.name if pods else None
