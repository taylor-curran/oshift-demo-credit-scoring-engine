# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine application in compliance with k8s standards Rules 02-06.

## Standards Compliance

### Rule 02 - Security Context
- ✅ `runAsNonRoot: true` - All containers run as non-root user (1001)
- ✅ `seccompProfile.type: RuntimeDefault` - Runtime default seccomp profile applied
- ✅ `readOnlyRootFilesystem: true` - Root filesystem is read-only
- ✅ `capabilities.drop: ["ALL"]` - All capabilities dropped for security

### Rule 03 - Image Provenance
- ✅ Tag pinning - Uses specific version tag with SHA digest
- ✅ Registry allowlist - Uses `registry.bank.internal` approved registry
- ✅ Signed images - Production images require Cosign signature verification

### Rule 04 - Naming & Labels
- ✅ Mandatory labels: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/part-of`, `environment`, `managed-by`
- ✅ Release name prefix: `pe-eng-credit-scoring-engine-prod` follows `<team>-<app>-<env>` pattern

### Rule 05 - Logging & Observability
- ✅ Prometheus annotations: `prometheus.io/scrape: "true"`, `prometheus.io/port: "8080"`
- ✅ JSON structured logging to stdout (Spring Boot default)
- ✅ ServiceMonitor for Prometheus metrics collection

### Rule 06 - Health Probes
- ✅ Liveness probe: `/actuator/health/liveness` endpoint
- ✅ Readiness probe: `/actuator/health/readiness` endpoint
- ✅ Proper timeouts and failure thresholds configured

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Configuration for ML models
- `ingress.yaml` - External access routing
- `servicemonitor.yaml` - Prometheus metrics collection

## Deployment

```bash
kubectl apply -f k8s/
```

## Resource Requirements

- CPU: 500m requests, 2000m limits
- Memory: 1536Mi requests, 3072Mi limits
- Replicas: 4 instances for high availability

## Key Compliance Features

### Security (Rule 02)
All containers run with enhanced security contexts:
- Non-root user execution (UID 1001)
- Read-only root filesystem with writable volumes for /tmp and /app/logs
- All Linux capabilities dropped
- Runtime default seccomp profile

### Image Security (Rule 03)
- Images sourced from approved `registry.bank.internal` registry
- Version pinning with SHA256 digest for immutability
- Cosign signature verification enforced by OpenShift Image Policies

### Observability (Rule 05)
- Prometheus metrics exposed on `/actuator/prometheus` endpoint
- ServiceMonitor configured for automatic metrics collection
- JSON structured logging to stdout for centralized log aggregation

### Health Monitoring (Rule 06)
- Spring Boot Actuator health endpoints for liveness and readiness
- Optimized probe timings for JVM applications
- Proper failure thresholds to prevent unnecessary restarts
