# Kubernetes Deployment - Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine with full compliance to organizational k8s-standards-library (Rules 01-06).

## Files

- `deployment.yaml` - Main application deployment with security context, resource limits, and health probes
- `service.yaml` - ClusterIP service with Prometheus annotations for observability
- `configmap.yaml` - ML model configuration data

## Standards Compliance

### ✅ Rule 01 - Resource Limits
- CPU requests: 1200m, limits: 2000m
- Memory requests: 1228Mi, limits: 2048Mi
- Requests ≈ 60% of limits for HPA headroom

### ✅ Rule 02 - Security Context
- `runAsNonRoot: true` (pod and container level)
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### ✅ Rule 03 - Image Provenance
- SHA-pinned image: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:7d865e959b24...`
- No `:latest` tags
- Approved registry: `registry.bank.internal`

### ✅ Rule 04 - Naming & Labels
- Consistent naming: `pe-eng-credit-scoring-engine-prod`
- All mandatory labels present:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### ✅ Rule 05 - Logging & Observability
- Prometheus annotations: `prometheus.io/scrape: "true"`
- Metrics port: `prometheus.io/port: "8080"`
- Applied to both service and pod templates

### ✅ Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness`
- Readiness probe: `/actuator/health/readiness`
- Proper timing configuration

## Deployment

```bash
kubectl apply -f k8s/
```

## Verification

```bash
# Check pod status
kubectl get pods -l app.kubernetes.io/name=credit-scoring-engine

# Check service
kubectl get svc pe-eng-credit-scoring-engine-prod

# Test health endpoints
kubectl port-forward deployment/pe-eng-credit-scoring-engine-prod 8080:8080
curl localhost:8080/actuator/health/liveness
curl localhost:8080/actuator/health/readiness
```
