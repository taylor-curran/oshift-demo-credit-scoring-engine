# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that are compliant with the k8s-standards library (Rules 01-06).

## Standards Compliance

### ✅ Rule 01 - Resource Requests & Limits
- All containers have CPU and memory requests and limits defined
- Requests are set to ~75% of limits for optimal scheduling
- Memory limit: 2048Mi, CPU limit: 2000m (2 vCPU)

### ✅ Rule 02 - Pod Security Baseline  
- `runAsNonRoot: true` - Containers run as non-root user
- `seccompProfile.type: RuntimeDefault` - Secure computing mode enabled
- `readOnlyRootFilesystem: true` - Root filesystem is read-only
- `capabilities.drop: ["ALL"]` - All dangerous capabilities dropped

### ✅ Rule 03 - Immutable, Trusted Images
- No `:latest` tags used - pinned to specific version with SHA digest
- Images from approved registry: `registry.bank.internal/*`
- SHA256 digest included for immutable image references

### ✅ Rule 04 - Naming & Label Conventions
- Release name follows pattern: `pe-eng-credit-scoring-engine-prod`
- All mandatory labels present:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### ✅ Rule 05 - Logging & Observability (Bonus)
- Prometheus scraping annotations configured
- JSON structured logging enabled
- Health endpoints exposed via Spring Boot Actuator

### ✅ Rule 06 - Health Probes (Bonus)
- Liveness probe: `/actuator/health/liveness`
- Readiness probe: `/actuator/health/readiness`
- Proper timeouts and failure thresholds configured

## Deployment

```bash
kubectl apply -f k8s/
```

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Application configuration and logging setup
- `ingress.yaml` - External access via two hostnames
