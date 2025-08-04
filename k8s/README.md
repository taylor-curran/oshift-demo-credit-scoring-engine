# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s standards library requirements.

## Standards Compliance

### Rule 02 - Security Context ✅
- `runAsNonRoot: true` - Container runs as non-root user (UID 1001)
- `seccompProfile.type: RuntimeDefault` - Uses runtime default seccomp profile
- `readOnlyRootFilesystem: true` - Root filesystem is read-only
- `capabilities.drop: ["ALL"]` - All Linux capabilities are dropped

### Rule 03 - Image Provenance ✅
- Uses pinned image tag: `registry.bank.internal/credit-scoring-engine:3.1.0`
- No `:latest` tags used
- Images sourced from approved internal registry

### Rule 04 - Naming & Labels ✅
All resources include mandatory labels:
- `app.kubernetes.io/name: credit-scoring-engine`
- `app.kubernetes.io/version: "3.1.0"`
- `app.kubernetes.io/part-of: banking-platform`
- `environment: prod`
- `managed-by: helm`

### Rule 05 - Logging & Observability ✅
- Prometheus scraping enabled: `prometheus.io/scrape: "true"`
- Metrics port configured: `prometheus.io/port: "8080"`
- Metrics path specified: `prometheus.io/path: "/actuator/prometheus"`
- ServiceMonitor configured for Prometheus Operator

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness`
- Readiness probe: `/actuator/health/readiness`
- Appropriate timeouts and failure thresholds configured

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Configuration for ML models
- `ingress.yaml` - External access configuration
- `servicemonitor.yaml` - Prometheus monitoring configuration

## Resource Allocation

- CPU requests: 500m, limits: 2000m
- Memory requests: 2Gi, limits: 3Gi
- Matches Cloud Foundry configuration (3GB memory, 4 instances)

## Security Features

- Non-root execution (UID/GID 1001)
- Read-only root filesystem with writable `/tmp` volume
- All capabilities dropped for minimal attack surface
- Runtime default seccomp profile applied
