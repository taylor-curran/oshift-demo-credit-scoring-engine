# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the banking k8s standards:

## Standards Compliance

### Rule 01 - Resource Limits ✅
- CPU requests: 300m, limits: 2000m
- Memory requests: 1536Mi, limits: 3072Mi
- Follows 60% request-to-limit ratio for HPA headroom

### Rule 02 - Pod Security Baseline ✅
- `runAsNonRoot: true`
- `readOnlyRootFilesystem: true`
- `seccompProfile.type: RuntimeDefault`
- `capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance ✅
- Uses pinned image with SHA digest
- Internal registry: `registry.bank.internal/*`
- No `:latest` tags

### Rule 04 - Naming & Labels ✅
- Proper naming: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: openshift`

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Configuration for ML models

## Deployment

```bash
kubectl apply -f k8s/
```

## Health Checks

The application exposes health checks at `/actuator/health/detailed` with:
- Liveness probe: 60s initial delay, 30s period
- Readiness probe: 30s initial delay, 10s period
