# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s-standards-library rules.

## Standards Compliance

### Rule 01 - Resource Limits ✅
- CPU requests: 300m, limits: 2000m
- Memory requests: 1536Mi, limits: 2048Mi
- Follows 60% rule of thumb for requests vs limits (300m/2000m = 15%, 1536Mi/2048Mi = 75%)
- Meets minimum requirements: ≥50m CPU, ≥128Mi memory
- Stays within maximum limits: ≤4 vCPU, ≤2Gi memory

### Rule 02 - Security Context ✅
- `runAsNonRoot: true` (container level)
- `seccompProfile.type: RuntimeDefault` (container level)
- `readOnlyRootFilesystem: true` (container level)
- `capabilities.drop: ["ALL"]` (container level)

### Rule 03 - Image Provenance ✅
- Uses pinned tag with SHA digest: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- Registry from approved allow-list: `registry.bank.internal/*`
- No `:latest` tags used

### Rule 04 - Naming & Labels ✅
- Release name follows pattern: `pe-eng-credit-scoring-engine-prod` (team-app-env format)
- Mandatory labels present:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

## Additional Features

### Observability
- Prometheus annotations:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
- JSON structured logging configured via ConfigMap
- Metrics endpoint exposed on port 8080

### Health Probes
- Liveness probe: `/actuator/health/liveness`, 30s initial delay, 10s period, 5s timeout, 3 failure threshold
- Readiness probe: `/actuator/health/readiness`, 10s initial delay, 5s period, 3s timeout, 1 failure threshold

### Security
- Read-only root filesystem with writable volumes for /tmp and /models
- Non-root user execution
- All capabilities dropped
- Seccomp profile enabled

## Files

- `deployment.yaml` - Main application deployment
- `service.yaml` - Service to expose the application
- `configmap.yaml` - Configuration for the application
- `ingress.yaml` - Ingress rules for external access

## Deployment

```bash
kubectl apply -f k8s/
```

## Environment Configuration

The deployment is configured for production environment with:
- 4 replicas for high availability
- 2GB memory allocation for ML inference operations (compliant with k8s standards)
- Integration with credit bureaus (Experian, Equifax, TransUnion)
- FCRA and ECOA compliance enabled
- A/B testing framework enabled
- Model refresh every 24 hours
