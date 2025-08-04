# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s standards (Rules 01-06).

## Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
- CPU requests: 600m (60% of 1000m limit)
- Memory requests: 1843Mi (60% of 3072Mi limit)
- All containers have both requests and limits defined
- Follows "requests ≈ 60% of limits" guideline for HPA headroom

### Rule 02 - Pod Security Baseline ✅
- `securityContext.runAsNonRoot: true`
- `securityContext.seccompProfile.type: RuntimeDefault`
- `securityContext.readOnlyRootFilesystem: true`
- `securityContext.capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance ✅
- Uses pinned image tag: `registry.bank.internal/credit-scoring-engine:3.1.0`
- No `:latest` tags
- Uses approved internal registry

### Rule 04 - Naming & Labels ✅
- Mandatory labels present on all resources:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### Rule 05 - Logging & Observability ✅
- Prometheus annotations for metrics scraping:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
- JSON logging configured in ConfigMap
- Metrics endpoint exposed on port 8080

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)

## Deployment

```bash
# Apply all manifests
kubectl apply -k k8s/

# Or apply individually
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/ingress.yaml
```

## Resource Limits

- CPU: 600m request, 1000m limit (60% ratio for HPA headroom)
- Memory: 1843Mi request, 3072Mi limit (60% ratio, matching Cloud Foundry 3GB allocation)
- Replicas: 4 (matching Cloud Foundry configuration)
- Fluent-bit sidecar: 120m CPU request, 200m limit; 154Mi memory request, 256Mi limit
