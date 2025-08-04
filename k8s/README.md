# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the banking platform's k8s standards.

## Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
- CPU requests: 600m, limits: 1000m
- Memory requests: 1228Mi, limits: 2048Mi
- Requests set to ~60% of limits for HPA headroom

### Rule 02 - Pod Security Baseline ✅
- `securityContext.runAsNonRoot: true`
- `securityContext.seccompProfile.type: RuntimeDefault`
- `securityContext.readOnlyRootFilesystem: true`
- `securityContext.capabilities.drop: ["ALL"]`

### Rule 03 - Immutable, Trusted Images ✅
- Image pinned with digest: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- No `:latest` tags used
- Internal registry source

### Rule 04 - Naming & Label Conventions ✅
- Release name: `pe-eng-credit-scoring-engine-prod`
- Required labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### Rule 05 - Logging & Observability ✅
- Prometheus annotations for metrics scraping:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
  - `prometheus.io/path: "/metrics"`
- Fluent-bit sidecar for log aggregation
- Metrics endpoint exposed on port 8080 at /metrics path

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)
- Detailed health check: `/actuator/health/detailed`

## Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/

# Or apply individually
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

## Resource Limits

- Main container: CPU 600m-1000m, Memory 1228Mi-2048Mi (Rule 01 compliant: ≤ 4vCPU/2Gi)
- Fluent-bit sidecar: CPU 50m-100m, Memory 64Mi-128Mi
- Replicas: 4 (matching Cloud Foundry configuration)
