# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s-standards-library requirements.

## Standards Compliance

### Rule 02 - Security Context
- ✅ `runAsNonRoot: true` - All containers run as non-root user
- ✅ `seccompProfile.type: RuntimeDefault` - Uses runtime default seccomp profile
- ✅ `readOnlyRootFilesystem: true` - Root filesystem is read-only
- ✅ `capabilities.drop: ["ALL"]` - All capabilities are dropped

### Rule 03 - Image Provenance
- ✅ Tag pinning with SHA digest - Uses `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- ✅ Registry allow-list - Uses approved `registry.bank.internal` registry
- ✅ No `:latest` tags - Specific version tags with digest

### Rule 04 - Naming & Labels
- ✅ Mandatory labels present:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`
- ✅ Release-name prefix: `pe-eng-credit-scoring-engine-prod`

### Rule 05 - Logging & Observability
- ✅ Prometheus annotations for metrics scraping
- ✅ Structured logging via Spring Boot JSON format
- ✅ Metrics endpoint on port 8080

### Rule 06 - Health Probes
- ✅ Liveness probe: `/actuator/health/liveness`
- ✅ Readiness probe: `/actuator/health/readiness`
- ✅ Proper timeouts and failure thresholds

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing HTTP and management ports
- `configmap.yaml` - Configuration for ML models and application settings

## Deployment

```bash
kubectl apply -f k8s/
```

## Notes

- The image SHA digest is a placeholder and should be updated with the actual digest
- ML model data in ConfigMap is a placeholder - consider using persistent volumes or object storage for production
- Environment variables match the original Cloud Foundry configuration
- Resource limits are set based on the original 3GB memory allocation
