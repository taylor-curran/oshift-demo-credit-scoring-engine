# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that are compliant with the banking k8s standards.

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service for internal communication
- `configmap.yaml` - Environment variables and configuration

## Standards Compliance

These manifests comply with all required k8s standards:

### Rule 01 - Resource Limits & Requests
- CPU requests: 600m, limits: 1000m
- Memory requests: 1843Mi, limits: 3072Mi
- Follows 60% rule of thumb for requests vs limits

### Rule 02 - Security Context
- `runAsNonRoot: true`
- `readOnlyRootFilesystem: true`
- `seccompProfile.type: RuntimeDefault`
- `capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance
- Uses pinned image with SHA digest
- Registry: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`

### Rule 04 - Naming & Labels
- Mandatory labels: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/part-of`, `environment`, `managed-by`
- Naming convention: `pe-eng-credit-scoring-engine-prod`

### Rule 05 - Observability
- Prometheus scraping annotations
- JSON logging to stdout (handled by application)

### Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness` (30s initial delay)
- Readiness probe: `/actuator/health/readiness` (10s initial delay)

## Deployment

```bash
kubectl apply -f k8s/
```

## Migration from Cloud Foundry

These manifests replace the Cloud Foundry `manifest.yml` configuration with equivalent Kubernetes resources.
