# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with all k8s standards rules:

## Standards Compliance

### ✅ Rule 01 - Resource Limits
- All containers have CPU and memory requests and limits defined
- Request-to-limit ratio maintained at ~60% for optimal resource utilization

### ✅ Rule 02 - Security Context
- `runAsNonRoot: true` - containers run as non-root user (1001)
- `seccompProfile.type: RuntimeDefault` - secure computing mode enabled
- `readOnlyRootFilesystem: true` - filesystem is read-only
- `capabilities.drop: ["ALL"]` - all dangerous capabilities dropped

### ✅ Rule 03 - Image Provenance
- Images use pinned SHA digests (no `:latest` tags)
- Images sourced from approved internal registry: `registry.bank.internal/*`

### ✅ Rule 04 - Naming & Labels
- Consistent naming convention: `pe-eng-credit-scoring-engine-prod`
- All mandatory labels present:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

## Deployment

Deploy using Kustomize:
```bash
kubectl apply -k k8s/
```

## Health Checks

The application includes:
- Liveness probe: `/actuator/health/liveness`
- Readiness probe: `/actuator/health/readiness`
- Prometheus metrics: annotations for scraping on port 8080
