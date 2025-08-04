# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine application in compliance with the k8s standards library (Rules 01-06).

## Standards Compliance

### Rule 01 - Resource Limits ✅
- CPU requests: 500m, limits: 2000m
- Memory requests: 1536Mi, limits: 3072Mi
- Follows 60% request-to-limit ratio for HPA headroom

### Rule 02 - Security Context ✅
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance ✅
- Uses pinned image tag with SHA digest
- Registry: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- No `:latest` tags used

### Rule 04 - Naming & Labels ✅
- Release name: `credit-scoring-engine-dev`
- Mandatory labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: banking-platform`
  - `environment: dev`
  - `managed-by: kubectl`

### Rule 05 - Logging & Observability ✅
- Prometheus annotations:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
- JSON structured logging configured
- Metrics endpoint exposed on port 8080

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failures)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure)

## Deployment

```bash
# Apply all manifests
kubectl apply -k .

# Or apply individually
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

## Verification

```bash
# Check deployment status
kubectl get pods -n banking-platform-dev -l app.kubernetes.io/name=credit-scoring-engine

# Check service endpoints
kubectl get svc -n banking-platform-dev credit-scoring-engine-dev

# Verify health probes
kubectl describe pod -n banking-platform-dev -l app.kubernetes.io/name=credit-scoring-engine

# Check Prometheus metrics
kubectl port-forward -n banking-platform-dev svc/credit-scoring-engine-dev 8080:8080
curl http://localhost:8080/metrics
```
