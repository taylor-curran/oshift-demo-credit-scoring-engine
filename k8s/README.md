# Kubernetes Deployment Manifests

This directory contains Kubernetes deployment manifests for the Credit Scoring Engine that comply with k8s-standards Rules 02-06.

## Standards Compliance

### Rule 02 - Pod Security Baseline ✅
- `runAsNonRoot: true` - Containers run as non-root user (1001)
- `seccompProfile.type: RuntimeDefault` - Runtime default seccomp profile applied
- `readOnlyRootFilesystem: true` - Root filesystem is read-only
- `capabilities.drop: ["ALL"]` - All Linux capabilities dropped

### Rule 03 - Image Provenance ✅
- Image uses pinned tag with SHA digest: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- Registry from approved allow-list: `registry.bank.internal/*`
- Production images require Cosign signature verification (handled by OpenShift Image Policies)

### Rule 04 - Naming & Labels ✅
- Release name follows pattern: `banking-credit-scoring-prod` (`<team>-<app>-<env>`)
- All mandatory labels present:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: banking-platform`
  - `environment: prod`
  - `managed-by: helm`

### Rule 05 - Logging & Observability ✅
- Prometheus scraping enabled: `prometheus.io/scrape: "true"`
- Metrics port configured: `prometheus.io/port: "8080"`
- Metrics path: `prometheus.io/path: "/actuator/prometheus"`
- JSON structured logging via Spring Boot Actuator

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness` (60s initial delay, 30s period)
- Readiness probe: `/actuator/health/readiness` (30s initial delay, 10s period)
- Spring Boot Actuator endpoints for JVM application health

## Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/

# Verify deployment
kubectl get pods -n credit-scoring
kubectl get svc -n credit-scoring
```

## Resource Configuration

- **CPU**: 500m requests, 2000m limits
- **Memory**: 2Gi requests, 3Gi limits  
- **Replicas**: 4 instances for high availability
- **JVM**: 2.5GB heap with G1GC and string deduplication

## Security Features

- Service account with `automountServiceAccountToken: false`
- Network policies restricting ingress/egress traffic
- Read-only root filesystem with writable volumes for `/tmp` and `/app/logs`
- Non-root user execution (UID 1001)
