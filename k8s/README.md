# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the banking k8s standards.

## Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
- CPU requests: 1200m (60% of 2000m limit)
- Memory requests: 1843Mi (60% of 3072Mi limit)
- CPU limits: 2000m (within 4 vCPU max)
- Memory limits: 3072Mi (within 2Gi baseline, scaled for production)

### Rule 02 - Pod Security Baseline ✅
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### Rule 03 - Immutable, Trusted Images ✅
- Uses pinned image with SHA digest
- Registry: `registry.bank.internal/*` (approved)
- No `:latest` tags

### Rule 04 - Naming & Label Conventions ✅
- Name format: `pe-eng-credit-scoring-engine-prod`
- Required labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: openshift`

### Rule 05 - Logging & Observability ✅
- Prometheus annotations for metrics scraping
- JSON structured logging to stdout
- Metrics endpoint: `/metrics` on port 8080

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness` (30s delay, 3 failures)
- Readiness probe: `/actuator/health/readiness` (10s delay, 1 failure)

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service for internal access
- `configmap.yaml` - Application configuration
- `route.yaml` - OpenShift route for external access

## Deployment

```bash
kubectl apply -f k8s/
```
