# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s standards:

## Standards Compliance

### Rule 01 - Resource Limits ✅
- CPU requests: 500m (0.5 vCPU)
- CPU limits: 2000m (2 vCPU) 
- Memory requests: 2Gi
- Memory limits: 3Gi
- Requests are 60% of limits for HPA headroom

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
- JSON stdout logs with fluent-bit sidecar for log shipping to Loki
- Prometheus metrics on port 8080 with `prometheus.io/scrape: "true"` annotations
- Structured logging forwarded to OpenShift Loki stack

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness` with optimized timings
- Readiness probe: `/actuator/health/readiness` for traffic routing
- Spring Boot Actuator endpoints for JVM application monitoring

## Files

- `deployment-dev.yaml` / `deployment-prod.yaml` - Main application deployment with 4 replicas
- `service-dev.yaml` / `service-prod.yaml` - ClusterIP service exposing port 8080
- `configmap-dev.yaml` / `configmap-prod.yaml` - Configuration for ML models
- `fluent-bit-configmap.yaml` / `fluent-bit-configmap-dev.yaml` - Log shipping configuration

## Migration from Cloud Foundry

These manifests replace the Cloud Foundry `manifest.yml` configuration with equivalent Kubernetes resources that meet enterprise security and operational standards.
