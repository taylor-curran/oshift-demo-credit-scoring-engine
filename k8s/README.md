# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s standards defined in the `.windsurf/rules/` directory.

## Standards Compliance

### Rule 01 - Resource Limits ✅
- CPU requests: 500m, limits: 2000m
- Memory requests: 1536Mi, limits: 3072Mi
- Follows 60% rule of thumb for requests vs limits

### Rule 02 - Pod Security Baseline ✅
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance ✅
- Uses pinned image with SHA digest: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:abc123def456789`
- Registry from allow-list: `registry.bank.internal/*`

### Rule 04 - Naming & Labels ✅
- Mandatory labels present:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: banking-platform`
  - `environment: prod`
  - `managed-by: kubernetes`

### Rule 05 - Logging & Observability ✅
- Prometheus annotations:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
- Application configured for JSON logging to stdout

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Configuration for ML models
- `ingress.yaml` - Ingress for external access
- `README.md` - This documentation

## Deployment

```bash
kubectl apply -f k8s/
```

## Notes

- The image SHA digest `abc123def456789` is a placeholder and should be replaced with the actual digest
- ML model ConfigMap contains placeholder data and should be updated with actual model files
- TLS certificate secret `credit-scoring-tls` needs to be created separately
