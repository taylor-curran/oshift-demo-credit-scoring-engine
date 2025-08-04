# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s standards (Rules 02-06).

## Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
- All containers have proper CPU and memory requests and limits
- Main container: 500m CPU request, 1000m CPU limit, 1228Mi memory request, 2048Mi memory limit
- Fluent-bit sidecar: 50m CPU request, 100m CPU limit, 64Mi memory request, 128Mi memory limit
- Follows 60% rule of thumb for requests vs limits

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
- Prometheus annotations for metrics scraping on all resources:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
- JSON structured logging configured in application.properties
- Fluent-bit sidecar for log shipping to OpenShift Loki stack
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

- CPU: 500m request, 1000m limit
- Memory: 1228Mi request, 2048Mi limit
- Replicas: 4 (matching Cloud Foundry configuration)
