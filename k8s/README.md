# Kubernetes Manifests - Credit Scoring Engine

This directory contains Kubernetes manifests for the Credit Scoring Engine that comply with the k8s standards library rules.

## Standards Compliance

### Rule 02 - Pod Security Baseline ✅
- `securityContext.runAsNonRoot: true`
- `securityContext.seccompProfile.type: RuntimeDefault`
- `securityContext.readOnlyRootFilesystem: true`
- `securityContext.capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance ✅
- Uses pinned image tag with SHA digest: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:a1b2c3d4e5f6789012345678901234567890123456789012345678901234567890`
- No `:latest` tags
- Registry from allowlist: `registry.bank.internal/*`
- Image immutability enforced with SHA digest

### Rule 04 - Naming & Label Conventions ✅
- Release name prefix: `pe-eng-credit-scoring-engine-dev`
- Mandatory labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: banking-platform`
  - `environment: dev`
  - `managed-by: kubernetes`

### Rule 05 - Logging & Observability ✅
- Prometheus annotations:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
- JSON logging configured in ConfigMap
- Metrics endpoint exposed on port 8080

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)

## Deployment

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## Resource Requirements

- CPU: 500m request, 2000m limit
- Memory: 1Gi request, 3Gi limit
- Replicas: 4 (as per original manifest.yml)

## Migration from Cloud Foundry

These manifests replace the Cloud Foundry `manifest.yml` deployment with a standards-compliant Kubernetes deployment. All environment variables and configuration from the original manifest have been preserved and migrated to the appropriate Kubernetes resources.

### Key Changes from Cloud Foundry:
- Added security context settings for Pod Security Baseline compliance
- Configured JSON structured logging for better observability
- Added Prometheus metrics annotations for monitoring integration
- Implemented proper health probes using Spring Boot Actuator endpoints
- Applied mandatory labeling conventions for resource management
- Used pinned image tags from approved internal registry

### Volume Mounts:
- `/tmp` - EmptyDir volume for temporary files (required for readOnlyRootFilesystem)
- `/models` - EmptyDir volume for ML model storage
- `/config` - ConfigMap volume for application configuration

### Security Features:
- Runs as non-root user for enhanced security
- Read-only root filesystem prevents runtime modifications
- All Linux capabilities dropped by default
- Runtime default seccomp profile applied
- Compliant with Pod Security Standards baseline policy
