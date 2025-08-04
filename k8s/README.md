# Kubernetes Manifests - K8s Standards Compliance

This directory contains Kubernetes manifests that comply with the k8s-standards-library Rules 01-04.

## Files Overview

- `namespace.yaml` - Dedicated namespace for the credit scoring engine
- `deployment.yaml` - Main application deployment with compliance fixes
- `service.yaml` - Service exposure with proper annotations
- `configmap.yaml` - Application configuration and Fluent-bit logging configuration
- `ingress.yaml` - Ingress rules for external access

## Standards Compliance

### Rule 01 - Resource Limits ✅
- **Main Container**: CPU requests: 500m, limits: 2000m; Memory requests: 1536Mi, limits: 2048Mi (2Gi)
- **JVM heap size**: 1536m (aligned with memory request to prevent OOMKilled errors)
- **Fluent-bit sidecar**: CPU 50m-200m, Memory 128Mi-256Mi
- Follows 60% rule of thumb for requests vs limits for HPA headroom

### Rule 02 - Security Context ✅
- **Pod-level security context**: `runAsNonRoot: true`, `runAsUser: 1001`, `runAsGroup: 1001`, `fsGroup: 1001`
- **Container-level security context**: 
  - `runAsNonRoot: true` - Prevents running as root user
  - `seccompProfile.type: RuntimeDefault` - Applies runtime default seccomp profile
  - `readOnlyRootFilesystem: true` - Makes root filesystem read-only
  - `capabilities.drop: ["ALL"]` - Drops all Linux capabilities
  - `allowPrivilegeEscalation: false` - Prevents privilege escalation

### Rule 03 - Image Provenance ✅
- Uses pinned image tags with SHA digests from approved registry
- **Main image**: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:7d865e959b2466f8239fcba23c8e76b2b32d4c16e168e7f0d5e7e8c9d1a2b3c4`
- **Fluent-bit image**: `registry.bank.internal/fluent-bit:2.1.0@sha256:b2c3d4e5f6789012345678901234567890123456789012345678901234567890a1`
- Registry from approved allow-list: `registry.bank.internal/*`
- No `:latest` tags used

### Rule 04 - Naming & Labels ✅
- **Release name prefix**: `pe-eng-credit-scoring-engine-prod` (team-app-env format)
- **Mandatory labels present on all resources**:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

## Additional Features

### Logging & Observability
- **Prometheus scraping annotations**: `prometheus.io/scrape: "true"`, `prometheus.io/port: "8080"`
- **Fluent-bit sidecar** for JSON log shipping to Loki
- **JSON structured logging** configured via ConfigMap
- **Metrics endpoint** exposed on port 8080

### Health Probes
- **Liveness probe**: `/actuator/health/liveness` (30s initial delay, 10s period, 5s timeout, 3 failure threshold)
- **Readiness probe**: `/actuator/health/readiness` (10s initial delay, 5s period, 3s timeout, 1 failure threshold)

## Deployment

```bash
kubectl apply -f k8s/
```

## Migration from Cloud Foundry

This replaces the existing `manifest.yml` Cloud Foundry configuration with proper Kubernetes manifests that meet enterprise security and operational standards.

## Important Notes

- **JVM Memory Alignment**: Fixed JVM heap size (-Xmx1536m) to align with container memory request (1536Mi) to prevent OOMKilled errors
- **Image SHA Digests**: The SHA digests in the manifests are placeholders and must be updated with actual image digests from your container registry
- **Security Impact**: The new security contexts (non-root, read-only filesystem) may impact application behavior if it attempts to write files or requires root privileges
- **Testing Required**: Thorough testing in a non-production environment is essential due to the security constraints
