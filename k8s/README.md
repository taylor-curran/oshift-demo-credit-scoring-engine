# Kubernetes Manifests - Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine in compliance with enterprise k8s standards (Rules 01-06).

## Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
- CPU requests: 600m, limits: 1000m
- Memory requests: 1228Mi, limits: 2048Mi
- Requests set to ~60% of limits for HPA headroom
- Fluent-bit sidecar: CPU 50m-100m, Memory 64Mi-128Mi

### Rule 02 - Pod Security Baseline ✅
- `securityContext.runAsNonRoot: true`
- `securityContext.seccompProfile.type: RuntimeDefault`
- `securityContext.readOnlyRootFilesystem: true`
- `securityContext.capabilities.drop: ["ALL"]`

### Rule 03 - Immutable, Trusted Images ✅
- Image pinned with digest: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- No `:latest` tags used
- Internal registry source
- Fluent-bit from approved registry: `quay.io/redhat-openshift-approved/*`

### Rule 04 - Naming & Label Conventions ✅
- Release name: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels present:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### Rule 05 - Logging & Observability ✅
- Prometheus annotations for metrics scraping:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
  - `prometheus.io/path: "/actuator/prometheus"`
- Fluent-bit sidecar for log aggregation
- JSON structured logging configured in application.properties
- Metrics endpoint exposed on port 8080 at /actuator/prometheus

### Rule 06 - Health Probe Configurations ✅
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)
- Spring Boot Actuator health endpoints enabled

## Deployment

```bash
# Apply all manifests
kubectl apply -k k8s/

# Or apply individually
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/fluent-bit-configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

## Configuration

### Environment Variables
- Database connection configured via ConfigMap and Secret
- Redis connection settings in ConfigMap
- Sensitive credentials (DB_USERNAME, DB_PASSWORD, REDIS_PASSWORD) in Secret

### Volumes
- `/tmp` - EmptyDir for temporary files (required for readOnlyRootFilesystem)
- `/models` - ConfigMap mount for ML model files
- `/fluent-bit/etc` - Fluent-bit configuration

### Networking
- Service exposes ports 8080 (HTTP) and 8081 (Actuator)
- Ingress configured for internal and external domains
- TLS termination with banking certificates

## Security Features
- Non-root user execution (UID 1001)
- Read-only root filesystem
- All capabilities dropped
- Seccomp profile enabled
- No privilege escalation allowed
