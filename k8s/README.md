# Kubernetes Deployment - Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine in compliance with organizational k8s standards (Rules 01-06).

## Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
- **CPU Requests**: 500m (0.5 vCPU)
- **CPU Limits**: 2000m (2 vCPU) 
- **Memory Requests**: 1843Mi (~60% of limit for HPA headroom)
- **Memory Limits**: 3072Mi (3GB as per original Cloud Foundry config)

### Rule 02 - Pod Security Baseline ✅
- `runAsNonRoot: true` - Prevents running as root user
- `seccompProfile.type: RuntimeDefault` - Applies runtime's default seccomp profile
- `readOnlyRootFilesystem: true` - Makes root filesystem read-only
- `capabilities.drop: ["ALL"]` - Drops all Linux capabilities
- Writable volumes mounted at `/tmp` and `/models` for application needs

### Rule 03 - Image Provenance ✅
- Uses pinned image tag: `registry.bank.internal/credit-scoring-engine:3.1.0`
- Includes SHA256 digest for immutability
- Sources from approved internal registry (`registry.bank.internal/*`)
- No `:latest` tags used

### Rule 04 - Naming & Label Conventions ✅
- **Release name prefix**: `banking-team-credit-scoring-engine-prod`
- **Mandatory labels**:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: banking-platform`
  - `environment: prod`
  - `managed-by: helm`

### Rule 05 - Logging & Observability ✅
- **Prometheus annotations**:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
- Metrics exposed on port 8080 at `/metrics` endpoint
- JSON structured logging configured via Spring Boot properties
- Health endpoints exposed via Spring Actuator

### Rule 06 - Health Probes ✅
- **Liveness Probe**: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- **Readiness Probe**: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)
- Uses Spring Boot Actuator health endpoints for JVM applications

## Deployment

### Using kubectl
```bash
kubectl apply -k k8s/
```

### Using kustomize
```bash
kustomize build k8s/ | kubectl apply -f -
```

## Configuration

The application configuration is managed through:
- **ConfigMap**: `credit-scoring-engine-config-prod` - Spring Boot properties
- **Environment Variables**: All original Cloud Foundry env vars preserved
- **Service Bindings**: Database and Redis connections via Kubernetes services

## Monitoring

- **Metrics**: Automatically scraped by Prometheus via annotations
- **Logs**: JSON structured logs to stdout, collected by fluent-bit sidecar
- **Health**: Liveness and readiness probes ensure application availability
- **Observability**: Service auto-appears in Grafana dashboards

## Security

- Non-root execution with dropped capabilities
- Read-only root filesystem with writable volumes for temp/models
- Seccomp profile applied for syscall filtering
- Image provenance verified through internal registry and SHA pinning
