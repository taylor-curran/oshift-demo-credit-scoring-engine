# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests for the Credit Scoring Engine application that are fully compliant with k8s-standards-library Rules 01-06.

## Standards Compliance

### Rule 01 - Resource Limits
- All containers have CPU and memory requests and limits defined
- Production: 500m-2000m CPU, 1536Mi-3072Mi memory
- Development: 100m-500m CPU, 256Mi-512Mi memory

### Rule 02 - Security Context
- `runAsNonRoot: true` - Containers run as non-root user
- `seccompProfile.type: RuntimeDefault` - Default seccomp profile applied
- `readOnlyRootFilesystem: true` - Root filesystem is read-only
- `capabilities.drop: ["ALL"]` - All Linux capabilities dropped

### Rule 03 - Image Provenance
- Images use pinned tags with SHA256 digests
- Images sourced from approved registry: `registry.bank.internal`
- No `:latest` tags used

### Rule 04 - Naming and Labels
- Consistent naming pattern: `banking-credit-scoring-{env}`
- Mandatory labels applied:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: {dev|prod}`
  - `managed-by: kubernetes`

### Rule 05 - Logging and Observability
- Prometheus scraping enabled with annotations:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
- Application configured for JSON logging to stdout
- Metrics exposed on port 8080

### Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)
- Uses Spring Boot Actuator endpoints

## Files

- `namespace.yaml` - Namespace definition with proper labels
- `deployment.yaml` - Production deployment (4 replicas, 3GB memory)
- `service.yaml` - Production service
- `deployment-dev.yaml` - Development deployment (1 replica, 512MB memory)
- `service-dev.yaml` - Development service

## Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/

# Apply specific environment
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment-dev.yaml
kubectl apply -f k8s/service-dev.yaml
```

## Volume Mounts

The deployment includes volume mounts for:
- `/tmp` - Temporary files (emptyDir)
- `/models` - ML model storage (emptyDir)

These volumes support the `readOnlyRootFilesystem: true` security requirement while providing writable directories where needed.
