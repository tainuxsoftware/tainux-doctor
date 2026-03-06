from kubernetes.client import CoreV1Api


def get_related_events(api: CoreV1Api, namespace: str, pod_name: str):
    field_selector = f"involvedObject.name={pod_name}"
    return api.list_namespaced_event(namespace=namespace, field_selector=field_selector).items
