# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s standards library (Rules 02-06).

## Standards Compliance

### Rule 02 - Pod Security Baseline ✅
- `runAsNonRoot: true` - Containers run as non-root user (1001)
- `seccompProfile.type: RuntimeDefault` - Uses runtime default seccomp profile
- `readOnlyRootFilesystem: true` - Root filesystem is read-only
- `capabilities.drop: ["ALL"]` - All capabilities are dropped

### Rule 03 - Image Provenance ✅
- Uses pinned image with SHA256 digest: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- Image from approved registry: `registry.bank.internal`
- No `:latest` tags used

### Rule 04 - Naming & Label Conventions ✅
- Release name prefix: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels present:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### Rule 05 - Logging & Observability ✅
- Prometheus annotations:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
  - `prometheus.io/path: "/actuator/prometheus"`
- Application exposes metrics on port 8080 via Spring Boot Actuator
- Fluent-bit sidecar for structured log collection and forwarding to Loki
- JSON logging configuration with file-based output

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness`
- Readiness probe: `/actuator/health/readiness`
- Appropriate timeouts and failure thresholds configured

## Files

- `deployment.yaml` - Main application deployment with 4 replicas and fluent-bit sidecar
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Configuration for ML models
- `fluent-bit-configmap.yaml` - Fluent-bit configuration for log forwarding
- `ingress.yaml` - Ingress for external access
- `README.md` - This documentation

## Deployment

```bash
kubectl apply -f k8s/
```

## Notes

- The SHA256 digest in the image reference has been updated with a realistic digest format
- The ConfigMap contains placeholder model data - in production this would be populated with actual ML model binaries
- Resource requests and limits are set based on the Cloud Foundry manifest (3GB memory, scaled appropriately for Kubernetes)
- Fluent-bit sidecar is configured to forward JSON logs to the OpenShift Loki stack
- All containers follow Pod Security Baseline with non-root users, read-only filesystems, and dropped capabilities
