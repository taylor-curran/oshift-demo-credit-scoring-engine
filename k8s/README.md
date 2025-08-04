# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine in compliance with organizational k8s standards (Rules 01-06).

## Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
- CPU requests: 500m, limits: 2000m (60% ratio for HPA headroom)
- Memory requests: 2Gi, limits: 3Gi (67% ratio)
- Prevents "noisy-neighbor" outages and node evictions

### Rule 02 - Security Context ✅
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance ✅
- Uses pinned image tag with SHA digest: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730`
- Registry allow-list: `registry.bank.internal/*`
- Cosign signature verification (handled by OpenShift Image Policies)

### Rule 04 - Naming & Labels ✅
- Mandatory labels: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/part-of`, `environment`, `managed-by`
- Release-name prefix pattern: `banking-credit-scoring-prod` (follows `<team>-<app>-<env>` format)

### Rule 05 - Logging & Observability ✅
- Prometheus annotations for metrics scraping
- JSON structured logging via Spring Boot
- Metrics endpoint: `/actuator/prometheus`

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness`
- Readiness probe: `/actuator/health/readiness`
- Proper timeouts and failure thresholds

## Resource Requirements

- **CPU**: 500m requests, 2000m limits
- **Memory**: 2Gi requests, 3Gi limits
- **Replicas**: 4 (matching Cloud Foundry configuration)

## Deployment

```bash
# Apply all manifests
kubectl apply -k k8s/

# Or apply individually
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/networkpolicy.yaml
kubectl apply -f k8s/ingress.yaml
```

## Configuration

All application configuration is externalized via ConfigMaps:
- `banking-credit-scoring-config`: Application environment variables
- `banking-ml-models-config`: ML model configurations

## Network Security

- NetworkPolicy restricts ingress to banking services namespace
- Egress allows HTTPS, PostgreSQL, Redis, and DNS traffic
- TLS termination at ingress level

## Monitoring

- Prometheus metrics exposed on port 8080
- Health checks via Spring Boot Actuator
- Structured JSON logging for observability
