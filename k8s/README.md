# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes deployment manifests for the Credit Scoring Engine that comply with the bank's k8s standards.

## Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
- CPU requests: 300m, limits: 2000m
- Memory requests: 1536Mi, limits: 3072Mi
- Follows 60% request-to-limit ratio for HPA headroom

### Rule 02 - Pod Security Baseline ✅
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`
- Non-root user (1001) with proper group settings

### Rule 03 - Immutable, Trusted Images ✅
- Uses pinned image with SHA256 digest
- Registry: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:7d865e959b2466f8239fcda593d844e861101b5c26e5a9cd80743f8f6b9b7c2a`
- No `:latest` tags

### Rule 04 - Naming & Label Conventions ✅
- Release name: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Configuration for ML models
- `README.md` - This documentation

## Deployment

```bash
kubectl apply -f k8s/
```

### Rule 05 - Logging & Observability ✅
- Prometheus annotations on service for metrics scraping
- JSON structured logging to stdout (Spring Boot default)
- Metrics endpoint exposed at `/metrics` on port 8080

### Rule 06 - Liveness & Readiness Probes ✅
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 30s period)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 10s period)
- Proper failure thresholds: liveness=3, readiness=1

## Health Checks

The application exposes separate health check endpoints:
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 30s period)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 10s period)
