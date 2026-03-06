# Deploying on OKD 4.21

## Build images

```bash
podman build -t ghcr.io/tainuxsoftware/tainux-doctor-api:latest backend
podman build -t ghcr.io/tainuxsoftware/tainux-doctor-ui:latest frontend
podman push ghcr.io/tainuxsoftware/tainux-doctor-api:latest
podman push ghcr.io/tainuxsoftware/tainux-doctor-ui:latest
```

## Apply manifests

```bash
oc apply -f deploy/okd/namespace.yaml
oc apply -f deploy/okd/configmap.yaml
oc apply -f deploy/okd/secret-example.yaml
oc apply -f deploy/okd/rbac.yaml
oc apply -f deploy/okd/deployment-api.yaml
oc apply -f deploy/okd/service-api.yaml
oc apply -f deploy/okd/route-api.yaml
oc apply -f deploy/okd/deployment-ui.yaml
oc apply -f deploy/okd/service-ui.yaml
oc apply -f deploy/okd/route-ui.yaml
```

## Validate

```bash
oc get pods -n tainux-doctor
oc get route -n tainux-doctor
```
