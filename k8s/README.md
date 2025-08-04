# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the banking platform's k8s standards.

## Standards Compliance

These manifests implement all required k8s standards:

### Rule 01 - Resource Requests & Limits ✅
- CPU requests: 600m (60% of 1000m limit)
- Memory requests: 1843Mi (60% of 3072Mi limit)
- CPU limits: 1000m
- Memory limits: 3072Mi

### Rule 02 - Pod Security Baseline ✅
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### Rule 03 - Immutable, Trusted Images ✅
- Uses pinned image with SHA digest
- Registry: `registry.bank.internal/*`
- No `:latest` tags

### Rule 04 - Naming & Label Conventions ✅
- Release name: `pe-eng-credit-scoring-engine-prod`
- Required labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: openshift`

### Rule 05 - Logging & Observability ✅
- Prometheus annotations for metrics scraping
- JSON structured logging configured
- Metrics endpoint: `/metrics` on port 8080

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failures)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure)

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Application configuration
- `secret.yaml` - Database and Redis credentials (base64 encoded)

## Deployment

```bash
kubectl apply -f k8s/
```

## Migration from Cloud Foundry

This replaces the existing `manifest.yml` Cloud Foundry configuration with standards-compliant Kubernetes manifests.
