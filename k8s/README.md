# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes deployment manifests that are fully compliant with the k8s standards (Rules 01-06).

## Standards Compliance

### Rule 01 - Resource Limits ✅
- CPU requests: 500m, limits: 2000m
- Memory requests: 1536Mi, limits: 2048Mi
- Proper request/limit ratios for HPA headroom

### Rule 02 - Security Context ✅
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance ✅
- Uses pinned SHA digest (no :latest tags)
- Image from approved registry: `registry.bank.internal/*`
- Ready for Cosign signature verification

### Rule 04 - Naming & Labels ✅
- Release name prefix: `pe-eng-credit-scoring-engine-prod`
- All mandatory labels present:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### Rule 05 - Observability ✅
- Prometheus annotations: `prometheus.io/scrape: "true"`
- Metrics port: `prometheus.io/port: "8080"`
- JSON structured logging configured
- Spring Boot Actuator endpoints exposed

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness`
- Readiness probe: `/actuator/health/readiness`
- Proper timing configurations for JVM applications

## Deployment Order

1. `configmap.yaml` - Application configuration
2. `secret.yaml` - Sensitive credentials (replace placeholders!)
3. `ml-models-config.yaml` - ML model data
4. `ml-models-metadata.yaml` - Model metadata
5. `deployment.yaml` - Main application deployment
6. `service.yaml` - Service exposure

## Important Notes

- **Replace placeholder values** in `secret.yaml` before deployment
- **Update ML model data** in `ml-models-config.yaml` with real models
- **Verify image SHA** corresponds to actual built image
- All manifests follow Pod Security Baseline requirements
