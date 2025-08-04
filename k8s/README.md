# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the 6 k8s standards:

## Standards Compliance

### ✅ Rule 01 - Resource Requests & Limits
- CPU requests: 1800m (60% of 3000m limit)
- Memory requests: 1843Mi (60% of 3072Mi limit)
- CPU limits: 3000m
- Memory limits: 3072Mi

### ✅ Rule 02 - Pod Security Baseline
- `runAsNonRoot: true`
- `readOnlyRootFilesystem: true`
- `seccompProfile.type: RuntimeDefault`
- `capabilities.drop: ["ALL"]`

### ✅ Rule 03 - Immutable, Trusted Images
- Pinned image with SHA256 digest
- Uses approved registry: `registry.bank.internal`
- No `:latest` tags

### ✅ Rule 04 - Naming & Label Conventions
- Release name: `pe-eng-credit-scoring-engine-prod`
- Required labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: openshift`

### ✅ Rule 05 - Logging & Observability
- Prometheus annotations: `prometheus.io/scrape: "true"`, `prometheus.io/port: "8080"`
- JSON logging configuration in ConfigMap
- Metrics endpoint exposed at `/metrics`

### ✅ Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)

## Deployment

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/ -n pe-eng-credit-scoring-engine-prod
```

## Migration from Cloud Foundry

This replaces the original `manifest.yml` Cloud Foundry configuration with OpenShift/Kubernetes native resources.
