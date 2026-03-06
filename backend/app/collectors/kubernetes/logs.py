from kubernetes.client import CoreV1Api
from kubernetes.client.exceptions import ApiException


def get_pod_logs(api: CoreV1Api, namespace: str, pod_name: str, previous: bool = False) -> str:
    try:
        return api.read_namespaced_pod_log(
            name=pod_name,
            namespace=namespace,
            previous=previous,
            tail_lines=200,
            timestamps=True,
        )
    except ApiException:
        return ""
