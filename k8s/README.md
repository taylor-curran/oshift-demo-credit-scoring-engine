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
- JSON stdout logs via Spring Boot structured logging
- Prometheus metrics on port 8080 with proper annotations
- Fluent-bit sidecar for production log shipping to Loki
- Prometheus auto-discovery enabled

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness` for Spring Boot Actuator
- Readiness probe: `/actuator/health/readiness` for Spring Boot Actuator
- Proper timing configurations for JVM applications

## Files

### Development Environment
- `deployment-dev.yaml` - Development deployment with 4 replicas and basic monitoring
- `service-dev.yaml` - ClusterIP service exposing port 8080 for dev
- `configmap-dev.yaml` - Development ML model configuration

### Production Environment
- `deployment-prod.yaml` - Production deployment with fluent-bit sidecar for logging
- `service-prod.yaml` - ClusterIP service exposing port 8080 for prod
- `configmap-prod.yaml` - Production ML model configuration
- `fluent-bit-configmap.yaml` - Fluent-bit logging configuration

## Migration from Cloud Foundry

These manifests replace the Cloud Foundry `manifest.yml` configuration with equivalent Kubernetes resources that meet enterprise security and operational standards.
