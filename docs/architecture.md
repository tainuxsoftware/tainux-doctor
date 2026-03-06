# TAINUX Doctor Architecture

## Components

- UI: static frontend for submitting diagnostics
- API: FastAPI backend
- Diagnostics engine: pod-focused rules-based analysis
- Kubernetes collectors: pods, events and logs

## MVP flow

1. User submits a question
2. API selects a target pod
3. Backend collects pod status, events and logs
4. Analyzers classify likely root cause
5. API returns summary, evidence and recommendations
