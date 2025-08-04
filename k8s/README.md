# Kubernetes Manifests - Credit Scoring Engine

This directory contains Kubernetes manifests for the Credit Scoring Engine that comply with the k8s standards library rules.

## Standards Compliance

### Rule 02 - Pod Security Baseline ✅
- `securityContext.runAsNonRoot: true`
- `securityContext.seccompProfile.type: RuntimeDefault`
- `securityContext.readOnlyRootFilesystem: true`
- `securityContext.capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance ✅
- Uses pinned image tag: `registry.bank.internal/credit-scoring-engine:3.1.0`
- No `:latest` tags
- Registry from allowlist: `registry.bank.internal/*`

### Rule 04 - Naming & Label Conventions ✅
- Release name prefix: `credit-scoring-engine-dev`
- Mandatory labels (applied to ALL resources including namespace):
  - `app.kubernetes.io/name: credit-scoring-engine` (or `banking-platform` for namespace)
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: banking-platform`
  - `environment: dev`
  - `managed-by: kubernetes`

### Rule 05 - Logging & Observability ✅
- Prometheus annotations:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
- JSON logging configured in ConfigMap
- Metrics endpoint exposed on port 8080

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)

## Deployment

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## Resource Requirements

- CPU: 500m request, 2000m limit
- Memory: 1Gi request, 3Gi limit
- Replicas: 4 (as per original manifest.yml)
