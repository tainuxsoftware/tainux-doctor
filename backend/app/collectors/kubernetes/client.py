from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException


def get_core_v1_api() -> client.CoreV1Api:
    try:
        config.load_incluster_config()
    except ConfigException:
        config.load_kube_config()
    return client.CoreV1Api()
