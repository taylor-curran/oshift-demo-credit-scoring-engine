# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with all k8s standards (Rules 01-06):

## Files Overview

- `namespace.yaml` - Creates the credit-scoring namespace
- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Application configuration
- `secret.yaml` - Database and Redis credentials
- `ingress.yaml` - External access routing

## Standards Compliance

### Rule 01 - Resource Limits
- CPU requests: 1800m, limits: 3000m
- Memory requests: 1843Mi, limits: 3072Mi
- Follows 60% request-to-limit ratio for HPA headroom

### Rule 02 - Security Context
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance
- Uses pinned tag with SHA digest
- Registry: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- No `:latest` tags

### Rule 04 - Naming & Labels
- Release name: `credit-team-credit-scoring-engine-prod`
- Mandatory labels: app.kubernetes.io/name, version, part-of, environment, managed-by

### Rule 05 - Logging & Observability
- Prometheus annotations: `prometheus.io/scrape: "true"`, `prometheus.io/port: "8080"`
- JSON structured logging configured
- Metrics endpoint exposed on port 8080

### Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failures)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure)

## Deployment

```bash
kubectl apply -f k8s/
```

## Verification

```bash
# Check pod status
kubectl get pods -n credit-scoring

# Check service endpoints
kubectl get svc -n credit-scoring

# Verify health probes
kubectl describe pod -n credit-scoring -l app.kubernetes.io/name=credit-scoring-engine
```
