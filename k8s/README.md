# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes deployment manifests that comply with the banking platform's k8s standards.

## Standards Compliance

### ✅ Rule 01 - Resource Requests & Limits
- CPU requests: 1800m (60% of 3000m limit)
- Memory requests: 1843Mi (60% of 3072Mi limit)
- CPU limits: 3000m
- Memory limits: 3072Mi

### ✅ Rule 02 - Pod Security Baseline
- `runAsNonRoot: true` (pod and container level)
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### ✅ Rule 03 - Immutable, Trusted Images
- Image: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456`
- No `:latest` tags used
- Trusted internal registry

### ✅ Rule 04 - Naming & Label Conventions
- Name: `pe-eng-credit-scoring-engine-prod`
- Labels: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/part-of`, `environment`, `managed-by`

### ✅ Rule 05 - Logging & Observability
- Prometheus annotations: `prometheus.io/scrape: "true"`, `prometheus.io/port: "8080"`
- JSON logging configured in ConfigMap

### ✅ Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness` (30s delay, 3 failures)
- Readiness probe: `/actuator/health/readiness` (10s delay, 1 failure)

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Application configuration properties

## Deployment

```bash
kubectl apply -f k8s/
```
