# TAINUX Doctor

AI-powered troubleshooting platform for Kubernetes, OKD and OpenShift.

This repository contains a **testable MVP** for OKD 4.21 with:

- FastAPI backend
- Working Kubernetes diagnostics for pods
- Static web UI
- OKD/OpenShift manifests
- Helm chart
- GitHub Actions build workflows

## What this MVP can diagnose

- CrashLoopBackOff
- OOMKilled
- ImagePullBackOff / ErrImagePull
- Pending / scheduling issues
- Readiness or liveness probe failures
- Generic unhealthy pod situations

## Architecture

- `backend/`: FastAPI API and Kubernetes diagnostics engine
- `frontend/`: static UI served by NGINX unprivileged
- `deploy/okd/`: manifests ready for OKD 4.21
- `helm/tainux-doctor/`: Helm chart
- `.github/workflows/`: CI examples

## Local backend run

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

## Local UI run

```bash
cd frontend
python -m http.server 8081
```

Then open `http://localhost:8081` and point API URL to `http://localhost:8080`.

## API

### Health

```bash
curl http://localhost:8080/health
```

### Diagnose

```bash
curl -X POST http://localhost:8080/api/v1/diagnose \
  -H "Content-Type: application/json" \
  -d '{
    "question":"Why is my pod crashing?",
    "namespace":"default",
    "resource_name":"my-pod"
  }'
```

## OKD 4.21 deploy

1. Build and push images
2. Edit image names in `deploy/okd/deployment-api.yaml` and `deployment-ui.yaml`
3. Apply:

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

## Notes

This is a **complete MVP**, not a finished enterprise platform. It is ready to deploy and start testing on OKD 4.21, and it is structured so you can evolve it into the larger TAINUX Doctor roadmap.
