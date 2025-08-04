# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s-standards-library rules.

## Compliance Summary

### ✅ Rule 01 - Resource Limits
- CPU requests: 500m, limits: 2000m
- Memory requests: 1536Mi, limits: 3072Mi
- Follows 60% request-to-limit ratio guideline

### ✅ Rule 02 - Security Context
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### ✅ Rule 03 - Image Provenance
- Uses pinned tag with SHA digest: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- No `:latest` tags
- Uses trusted internal registry

### ✅ Rule 04 - Naming & Labels
- Mandatory labels present:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`
- Release name follows pattern: `banking-credit-scoring-prod`

### ✅ Rule 05 - Logging & Observability
- Prometheus annotations:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
- Structured JSON logging configured
- Metrics endpoint exposed on port 8080

### ✅ Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness` with 30s initial delay
- Readiness probe: `/actuator/health/readiness` with 10s initial delay
- Proper failure thresholds configured

## Files

- `deployment.yaml` - Main application deployment
- `service.yaml` - Service definition
- `configmap.yaml` - Application configuration
- `ingress.yaml` - Ingress routing configuration
- `README.md` - This documentation

## Deployment

```bash
kubectl apply -f k8s/
```

## Verification

```bash
# Check deployment status
kubectl get deployment banking-credit-scoring-prod

# Check pod security context
kubectl describe pod -l app.kubernetes.io/name=credit-scoring-engine

# Verify health probes
kubectl get pods -l app.kubernetes.io/name=credit-scoring-engine -o yaml | grep -A 10 "livenessProbe\|readinessProbe"

# Check Prometheus annotations
kubectl get service banking-credit-scoring-prod -o yaml | grep prometheus
```
