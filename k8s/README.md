# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the banking platform's k8s standards.

## Standards Compliance

### ✅ Rule 01 - Resource Requests & Limits
- CPU requests: 600m (60% of 1000m limit)
- Memory requests: 1843Mi (60% of 3072Mi limit)
- CPU limits: 1000m
- Memory limits: 3072Mi

### ✅ Rule 02 - Pod Security Baseline
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### ✅ Rule 03 - Immutable, Trusted Images
- Image: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- No `:latest` tags used
- Trusted internal registry

### ✅ Rule 04 - Naming & Label Conventions
- Release name: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: openshift`

### ✅ Rule 05 - Logging & Observability
- Prometheus annotations:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`

### ✅ Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness` (30s initial delay)
- Readiness probe: `/actuator/health/readiness` (10s initial delay)

## Deployment

```bash
kubectl apply -k k8s/
```

## Files

- `namespace.yaml` - Credit scoring namespace
- `configmap.yaml` - Application configuration
- `ml-models-configmap.yaml` - ML model configuration
- `deployment.yaml` - Main application deployment
- `service.yaml` - Service definition
- `ingress.yaml` - External access configuration
- `kustomization.yaml` - Kustomize configuration
