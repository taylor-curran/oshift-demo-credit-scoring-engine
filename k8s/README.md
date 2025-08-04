# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s standards library (Rules 02-06).

## Standards Compliance

### Rule 02 - Security Context Baseline ✅
- `runAsNonRoot: true` - All containers run as non-root user (1001)
- `seccompProfile.type: RuntimeDefault` - Applied at pod and container level
- `readOnlyRootFilesystem: true` - Root filesystem is read-only
- `capabilities.drop: ["ALL"]` - All Linux capabilities dropped

### Rule 03 - Image Provenance ✅
- No `:latest` tags used
- Images from approved registry: `registry.bank.internal/*`
- SHA256 digest pinning for immutable deployments

### Rule 04 - Naming & Label Conventions ✅
- Release name prefix: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels applied to all resources:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### Rule 05 - Logging & Observability ✅
- Prometheus scraping enabled: `prometheus.io/scrape: "true"`
- Metrics port configured: `prometheus.io/port: "8080"`
- Metrics path: `prometheus.io/path: "/actuator/prometheus"`
- JSON logging via Spring Boot Actuator

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness`
- Readiness probe: `/actuator/health/readiness`
- Appropriate timeouts and failure thresholds configured

## Deployment

```bash
kubectl apply -f k8s/
```

## Resource Requirements

- 4 replicas for high availability
- 2Gi memory requests, 3Gi limits
- 500m CPU requests, 2000m CPU limits
- Read-only root filesystem with writable /tmp volume
