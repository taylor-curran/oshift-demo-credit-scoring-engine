# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the banking organization's k8s standards.

## Standards Compliance

### ✅ Rule 01 - Resource Requests & Limits
- CPU requests: 500m (0.5 vCPU)
- CPU limits: 2000m (2 vCPU) 
- Memory requests: 1536Mi (~1.5 GB)
- Memory limits: 3072Mi (3 GB)
- Requests set to ~75% of limits for HPA headroom

### ✅ Rule 02 - Pod Security Baseline
- `runAsNonRoot: true` - Prevents running as root user
- `seccompProfile.type: RuntimeDefault` - Applies default seccomp profile
- `readOnlyRootFilesystem: true` - Makes root filesystem read-only
- `capabilities.drop: ["ALL"]` - Drops all Linux capabilities

### ✅ Rule 03 - Image Provenance
- Uses pinned image with SHA digest: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:7d865e959b2466f8239fcda593d120e1e32dc6d15540478e6a0b2a45aaa21eba`
- No `:latest` tags used
- Images from trusted internal registry

### ✅ Rule 04 - Naming & Label Conventions
- Release name: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: openshift`

### ✅ Rule 05 - Logging & Observability
- Prometheus scraping annotations:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
- Application configured for JSON logging to stdout

### ✅ Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Configuration for ML models
- `route.yaml` - OpenShift routes for external access

## Migration from Cloud Foundry

This replaces the Cloud Foundry `manifest.yml` with standards-compliant Kubernetes resources:

| CF Manifest | Kubernetes Equivalent |
|-------------|----------------------|
| `instances: 4` | `replicas: 4` |
| `memory: 3072M` | `resources.limits.memory: 3072Mi` |
| `env:` | `env:` in container spec |
| `services:` | External service references (not included) |
| `routes:` | OpenShift Route resources |
| `health-check-*` | `livenessProbe` and `readinessProbe` |

## Deployment

```bash
kubectl apply -f k8s/
```
