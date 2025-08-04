# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s standards (Rules 01-06).

## Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
- CPU: 500m request, 1000m limit
- Memory: 1228Mi request, 2048Mi limit
- Fluent-bit sidecar: 50m/100m CPU, 64Mi/128Mi memory

### Rule 02 - Pod Security Baseline ✅
- `securityContext.runAsNonRoot: true`
- `securityContext.seccompProfile.type: RuntimeDefault`
- `securityContext.readOnlyRootFilesystem: true`
- `securityContext.capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance ✅
- Uses pinned image tag with SHA digest: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- No `:latest` tags
- Uses approved internal registry and Red Hat approved registry for fluent-bit

### Rule 04 - Naming & Labels ✅
- Mandatory labels present on all resources:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`
- Release-name prefix: `pe-eng-credit-scoring-engine-prod`

### Rule 05 - Logging & Observability ✅
- Prometheus annotations for metrics scraping:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
- JSON logging configured in application.properties
- Fluent-bit sidecar for log shipping to Loki
- Metrics endpoint exposed on port 8080

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)

## Deployment

```bash
# Apply all manifests using Kustomize
kubectl apply -k k8s/

# Or apply individually
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/fluent-bit-configmap.yaml
kubectl apply -f k8s/ingress.yaml
```

## Architecture

- **Main Container**: Credit Scoring Engine (Spring Boot)
- **Sidecar Container**: Fluent-bit for log shipping
- **Replicas**: 4 (matching Cloud Foundry configuration)
- **Security**: Non-root user, read-only filesystem, dropped capabilities
- **Observability**: Prometheus metrics, JSON logs shipped to Loki
