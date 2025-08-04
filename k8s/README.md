# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s standards:

## Standards Compliance

### Rule 01 - Resource Limits ✅
- Main app CPU: 500m requests, 2000m limits (25% ratio for HPA headroom)
- Main app Memory: 1536Mi/2Gi requests, 3072Mi/3Gi limits (dev/prod)
- Fluent-bit sidecar: 50m-100m CPU, 64Mi-128Mi memory
- All containers have proper resource constraints defined

### Rule 02 - Security Context ✅
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`
- `allowPrivilegeEscalation: false`

### Rule 03 - Image Provenance ✅
- Uses pinned tag with digest: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- No `:latest` tags
- Uses approved internal registry

### Rule 04 - Naming & Labels ✅
- Release name: `pe-eng-credit-scoring-engine-prod`
- Required labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### Rule 05 - Logging & Observability ✅
- JSON structured logging via fluent-bit sidecar (both dev and prod)
- Prometheus annotations: `prometheus.io/scrape: "true"`, `prometheus.io/port: "8080"`
- Logs forwarded to OpenShift Loki stack

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 30s period)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 10s period)
- Consistent configuration across dev and prod environments

## Files

### Development Environment
- `deployment-dev.yaml` - Development deployment with 4 replicas, fluent-bit sidecar for logging
- `service-dev.yaml` - ClusterIP service exposing port 8080 for dev
- `configmap-dev.yaml` - Development ML model configuration
- `fluent-bit-configmap-dev.yaml` - Fluent-bit logging configuration for dev

### Production Environment
- `deployment-prod.yaml` - Production deployment with fluent-bit sidecar for logging
- `service-prod.yaml` - ClusterIP service exposing port 8080 for prod
- `configmap-prod.yaml` - Production ML model configuration
- `fluent-bit-configmap.yaml` - Fluent-bit logging configuration

## Migration from Cloud Foundry

These manifests replace the Cloud Foundry `manifest.yml` configuration with equivalent Kubernetes resources that meet enterprise security and operational standards.
