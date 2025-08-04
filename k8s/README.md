# Kubernetes Manifests - Credit Scoring Engine

This directory contains Kubernetes manifests that are fully compliant with the k8s-standards-library Rules 01-06.

## Standards Compliance

### ✅ Rule 01 - Resource Limits
- **Production**: CPU requests 1200m (~60% of 2000m limit), Memory requests 1200Mi (~60% of 2Gi limit)
- **Development**: CPU requests 600m (~60% of 1000m limit), Memory requests 614Mi (~60% of 1Gi limit)
- **Fluent-bit sidecar**: CPU requests 60m (~60% of 100m limit), Memory requests 77Mi (~60% of 128Mi limit)
- All containers have proper resource requests and limits within organizational baselines

### ✅ Rule 02 - Security Context
- `runAsNonRoot: true` for all containers
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### ✅ Rule 03 - Image Provenance
- Images from approved registry: `registry.bank.internal/*`
- SHA-pinned images (no `:latest` tags)
- Cosign signature verification handled by OpenShift Image Policies

### ✅ Rule 04 - Naming & Labels
- **Mandatory labels**: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/part-of`, `environment`, `managed-by`
- **Consistent naming pattern**: `banking-eng-credit-scoring-engine-{env}` (follows `<team>-<app>-<env>` format)
- **Tool provenance**: `managed-by: helm` for consistent deployment tracking

### ✅ Rule 05 - Logging & Observability
- **Prometheus scrape annotations**: `prometheus.io/scrape: "true"`, `prometheus.io/port: "8080"`
- **Fluent-bit sidecar** for centralized logging to Loki
- **JSON structured logging** to stdout via `/app/logs/*.log`
- **Metrics endpoint**: `/actuator/prometheus` on port 8080

### ✅ Rule 06 - Health Probes
- **Liveness probe**: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- **Readiness probe**: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)
- **Spring Boot Actuator** endpoints for JVM application health monitoring

## Files

- `namespace.yaml` - Credit scoring namespace with proper labeling
- `deployment.yaml` - Production deployment (4 replicas)
- `deployment-dev.yaml` - Development deployment (2 replicas)
- `service.yaml` - Production service
- `service-dev.yaml` - Development service
- `fluent-bit-configmap-prod.yaml` - Production logging configuration
- `fluent-bit-configmap-dev.yaml` - Development logging configuration

## Deployment

```bash
# Deploy namespace first
kubectl apply -f k8s/namespace.yaml

# Deploy development environment
kubectl apply -f k8s/fluent-bit-configmap-dev.yaml
kubectl apply -f k8s/deployment-dev.yaml
kubectl apply -f k8s/service-dev.yaml

# Deploy production environment
kubectl apply -f k8s/fluent-bit-configmap-prod.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## Key Compliance Improvements

1. **Resource Optimization**: Adjusted CPU/memory requests to ~60% of limits per Rule 01 guidelines
2. **Security Hardening**: Full Pod Security Baseline compliance with non-root execution and capability dropping
3. **Image Security**: SHA-pinned images from approved internal registry
4. **Observability**: Comprehensive Prometheus metrics and structured logging via fluent-bit
5. **Health Monitoring**: Proper Spring Boot Actuator health probe configuration

## Notes

- All containers run as non-root with read-only filesystems
- Temporary files use emptyDir volumes mounted at `/tmp` and `/app/logs`
- Fluent-bit configuration points to internal Loki endpoints for log aggregation
- Resource requests follow the "requests ≈ 60% of limits" guideline for optimal HPA behavior
- Image SHA digests should be updated with actual values from your registry during deployment
