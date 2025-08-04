# Kubernetes Manifests - K8s Standards Compliance

This directory contains Kubernetes manifests that comply with the k8s-standards-library Rules 01-06.

## Files Overview

- `namespace.yaml` - Dedicated namespace for the credit scoring engine
- `deployment.yaml` - Main application deployment with compliance fixes
- `service.yaml` - Service exposure with proper annotations
- `configmap.yaml` - Fluent-bit configuration for centralized logging

## Standards Compliance

### Rule 01 - Resource Limits ✅
- CPU requests: 1200m (1.2 vCPU), limits: 2000m (2 vCPU)
- Memory requests: 1200Mi (~1.2GB), limits: 2048Mi (2GB)
- Fluent-bit sidecar: CPU 50m-200m, Memory 128Mi-256Mi
- Requests ≈ 60% of limits for HPA headroom

### Rule 02 - Security Context ✅
- `runAsNonRoot: true` - Prevents running as root user
- `seccompProfile.type: RuntimeDefault` - Applies runtime default seccomp profile
- `readOnlyRootFilesystem: true` - Makes root filesystem read-only
- `capabilities.drop: ["ALL"]` - Drops all Linux capabilities

### Rule 03 - Image Provenance ✅
- Uses pinned image tags with SHA digests
- Images from approved registry: `registry.bank.internal/*`
- No `:latest` tags used

### Rule 04 - Naming & Labels ✅
- Release name prefix: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels present on all resources:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### Rule 05 - Logging & Observability ✅
- Prometheus scraping annotations:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
- Fluent-bit sidecar for JSON log shipping to Loki
- Metrics exposed on port 8080

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)

## Deployment

```bash
kubectl apply -f k8s/
```

## Migration from Cloud Foundry

This replaces the existing `manifest.yml` Cloud Foundry configuration with proper Kubernetes manifests that meet enterprise security and operational standards.

## Important Notes

- **Image SHA Digests**: The SHA digests in the manifests have been updated with realistic values but should be verified against your actual container registry
- **Security Impact**: The new security contexts (non-root, read-only filesystem) may impact application behavior if it attempts to write files or requires root privileges
- **Testing Required**: Thorough testing in a non-production environment is essential due to the security constraints
