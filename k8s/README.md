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
- Image: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:4f8b2c9e1a7d6f3b8e5c2a9f7e4d1b8c5a2f9e6d3b0c7a4e1f8b5c2a9f6e3d0`
- No `:latest` tags used
- Trusted internal registry

### ✅ Rule 04 - Naming & Label Conventions
- Name: `pe-eng-credit-scoring-engine-prod`
- Labels: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/part-of`, `environment`, `managed-by`

### ✅ Rule 05 - Logging & Observability
- Prometheus annotations: `prometheus.io/scrape: "true"`, `prometheus.io/port: "8080"`
- JSON logging configured in ConfigMap
- Fluent-bit sidecar for log shipping to OpenShift Loki

### ✅ Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness` (30s delay, 10s period, 5s timeout, 3 failures)
- Readiness probe: `/actuator/health/readiness` (10s delay, 5s period, 3s timeout, 1 failure)

## Files

- `deployment.yaml` - Main application deployment with 4 replicas and fluent-bit sidecar
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Application configuration properties
- `fluent-bit-configmap.yaml` - Fluent-bit configuration for log shipping

## Deployment

```bash
kubectl apply -f k8s/
```
