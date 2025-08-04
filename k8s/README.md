# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes deployment manifests that are fully compliant with the k8s-standards-library Rules 01-06.

## Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
- CPU requests: 500m, limits: 2000m
- Memory requests: 1536Mi, limits: 2560Mi
- Follows 60% rule of thumb for requests vs limits

### Rule 02 - Pod Security Baseline ✅
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance ✅
- Uses pinned image with SHA digest: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- No `:latest` tags
- Uses approved registry: `registry.bank.internal/*`

### Rule 04 - Naming & Labels ✅
- Release name prefix: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### Rule 05 - Logging & Observability ✅
- Prometheus annotations:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
- Application configured for JSON logging to stdout
- Metrics exposed on port 8080

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Configuration for ML models
- `ingress.yaml` - Ingress rules for external access

## Deployment

```bash
kubectl apply -f k8s/
```

## Verification

```bash
# Check deployment status
kubectl get deployment pe-eng-credit-scoring-engine-prod

# Check pod security context
kubectl describe pod -l app.kubernetes.io/name=credit-scoring-engine

# Verify Prometheus scraping
kubectl get pods -l app.kubernetes.io/name=credit-scoring-engine -o yaml | grep prometheus.io

# Test health endpoints
kubectl port-forward svc/pe-eng-credit-scoring-engine-prod 8080:8080
curl http://localhost:8080/actuator/health/liveness
curl http://localhost:8080/actuator/health/readiness
```
