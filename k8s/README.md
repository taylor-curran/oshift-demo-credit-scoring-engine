# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes deployment manifests that comply with the k8s standards (Rules 02-06).

## Standards Compliance

### Rule 02 - Security Context ✅
- `runAsNonRoot: true` - Prevents running as root user
- `seccompProfile.type: RuntimeDefault` - Applies secure computing profile
- `readOnlyRootFilesystem: true` - Makes root filesystem read-only
- `capabilities.drop: ["ALL"]` - Drops all Linux capabilities

### Rule 03 - Image Provenance ✅
- Uses pinned version tag (3.1.0) instead of :latest
- References approved registry: `registry.bank.internal`
- Production deployments should use Cosign-signed images

### Rule 04 - Naming & Labels ✅
- Follows naming convention: `credit-scoring-engine-dev`
- Includes all mandatory labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: banking-platform`
  - `environment: dev`
  - `managed-by: kubernetes`

### Rule 05 - Logging & Observability ✅
- Prometheus scraping annotations:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
- Application configured for JSON logging to stdout
- Metrics endpoint exposed on port 8080

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)

## Files

- `deployment.yaml` - Main application deployment
- `service.yaml` - Service definition with proper labels and annotations
- `configmap.yaml` - Configuration for Spring Boot application

## Resource Allocation

Based on the original Cloud Foundry manifest (3GB memory, 4 instances):
- CPU requests: 500m, limits: 2000m
- Memory requests: 1536Mi, limits: 3072Mi
- 4 replicas for high availability
