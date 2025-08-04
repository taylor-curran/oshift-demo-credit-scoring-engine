# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine application in compliance with enterprise k8s standards.

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Environment variables and configuration

## Standards Compliance

These manifests comply with all required k8s standards:

### Rule 01 - Resource Limits
- CPU requests: 1800m (60% of 3000m limit)
- Memory requests: 1843Mi (60% of 3072Mi limit)
- Proper resource isolation for multi-tenant cluster

### Rule 02 - Security Context
- `runAsNonRoot: true` - No root execution
- `readOnlyRootFilesystem: true` - Immutable filesystem
- `capabilities.drop: ["ALL"]` - Minimal privileges
- `seccompProfile.type: RuntimeDefault` - Secure computing

### Rule 03 - Image Provenance
- Uses pinned image with SHA digest from internal registry
- No `:latest` tags for immutable deployments

### Rule 04 - Naming & Labels
- Follows `pe-eng-credit-scoring-engine-prod` naming pattern
- Mandatory labels: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/part-of`, `environment`, `managed-by`

### Rule 05 - Logging & Observability
- Prometheus scraping annotations on pods
- JSON structured logging to stdout
- Metrics endpoint at `/metrics` on port 8080

### Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness` (30s delay, 3 failures)
- Readiness probe: `/actuator/health/readiness` (10s delay, 1 failure)

## Deployment

```bash
kubectl apply -f k8s/
```

## Monitoring

The application exposes metrics at `/actuator/health/detailed` and `/metrics` for monitoring integration.
