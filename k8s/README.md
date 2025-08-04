# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine application in compliance with banking k8s standards.

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Non-sensitive configuration values
- `secret.yaml` - Sensitive configuration template (API keys, database credentials) - values populated by deployment pipeline

## Standards Compliance

These manifests comply with all required k8s standards:

### Rule 01 - Resource Requests & Limits
- CPU requests: 600m, limits: 1000m
- Memory requests: 1843Mi, limits: 3072Mi

### Rule 02 - Pod Security Baseline
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`
- `allowPrivilegeEscalation: false`

### Rule 03 - Image Provenance
- Uses pinned image with SHA digest from approved registry
- Image: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:7d865e959b2466f8239fcba23c8966c8c1eabd319d8e4f30fe9f8eba5c2b4b5d`

### Rule 04 - Naming & Labels
- Naming convention: `pe-eng-credit-scoring-engine-prod`
- All mandatory labels present:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: openshift`

## Deployment

```bash
kubectl apply -f k8s/
```

## Health Checks

The application includes comprehensive health probes:
- Startup probe: `/actuator/health`
- Liveness probe: `/actuator/health/liveness`
- Readiness probe: `/actuator/health/readiness`

## Security

- Runs as non-root user (UID 1001)
- Read-only root filesystem with writable volumes for `/tmp`, `/models`, and `/app/logs`
- All Linux capabilities dropped
- Seccomp profile enabled
