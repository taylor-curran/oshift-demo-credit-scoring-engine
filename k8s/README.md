# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s-standards-library rules.

## Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
- CPU requests: `500m` (0.5 vCPU)
- Memory requests: `2Gi`
- CPU limits: `2000m` (2 vCPU)
- Memory limits: `3Gi`
- Requests ≈ 60% of limits for HPA headroom

### Rule 02 - Pod Security Baseline ✅
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance ✅
- Uses pinned version tag: `registry.bank.internal/credit-scoring-engine:3.1.0`
- Image from approved registry: `registry.bank.internal/*`
- No `:latest` tags used
- Ready for production deployment once real images are built and pushed

### Rule 04 - Naming & Labels ✅
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
- JSON structured logging via Spring Boot Actuator

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness` (initialDelaySeconds: 30s, failureThreshold: 3)
- Readiness probe: `/actuator/health/readiness` (initialDelaySeconds: 10s, failureThreshold: 1)
- Startup probe configured for JVM applications

## Deployment

```bash
kubectl apply -f k8s/
```

## Files

- `namespace.yaml` - Creates credit-scoring namespace
- `configmap.yaml` - Application configuration
- `deployment.yaml` - Main application deployment
- `service.yaml` - ClusterIP service
- `ingress.yaml` - External access configuration
- `networkpolicy.yaml` - Network security policies
