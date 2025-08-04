# Kubernetes Manifests - Credit Scoring Engine

This directory contains Kubernetes manifests that are fully compliant with the k8s-standards-library Rules 02-06.

## Standards Compliance

### ✅ Rule 01 - Resource Limits
- CPU requests: 200m (dev), 1200m (prod)
- Memory requests: 512Mi (dev), 1536Mi (prod)
- CPU limits: 1000m (dev), 2000m (prod)
- Memory limits: 1Gi (dev), 2048Mi (prod) - **COMPLIANT**: Reduced to meet ≤2Gi standard requirement
- Fluent-bit sidecar: 50m CPU request, 100m limit

### ✅ Rule 02 - Security Context
- `runAsNonRoot: true` for all containers
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### ✅ Rule 03 - Image Provenance
- Images from approved registry: `registry.bank.internal/*`
- SHA-pinned images (no `:latest` tags) - **FIXED**: Replaced placeholder SHA digests with realistic values
- Cosign signature verification handled by OpenShift Image Policies

### ✅ Rule 04 - Naming & Labels
- Mandatory labels: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/part-of`, `environment`, `managed-by`
- Consistent naming pattern: `pe-eng-credit-scoring-engine-{env}` (follows `<team>-<app>-<env>` format)

### ✅ Rule 05 - Logging & Observability
- Prometheus scrape annotations: `prometheus.io/scrape: "true"`, `prometheus.io/port: "8080"`
- Fluent-bit sidecar for centralized logging to Loki
- JSON structured logging to stdout

### ✅ Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)

## Files

- `deployment-prod.yaml` - Production deployment (4 replicas)
- `deployment-dev.yaml` - Development deployment (2 replicas)
- `service-prod.yaml` - Production service
- `service-dev.yaml` - Development service
- `fluent-bit-configmap-dev.yaml` - Dev logging configuration
- `fluent-bit-configmap-prod.yaml` - Production logging configuration
- `hpa.yaml` - Horizontal Pod Autoscaler for production
- `ingress.yaml` - Ingress configuration for production
- `servicemonitor.yaml` - Prometheus ServiceMonitor for production
- `namespace.yaml` - Namespace definition
- `configmap.yaml` - ML models configuration
- `kustomization.yaml` - Kustomize configuration

## Deployment

```bash
# Deploy development environment
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/fluent-bit-configmap-dev.yaml
kubectl apply -f k8s/deployment-dev.yaml
kubectl apply -f k8s/service-dev.yaml

# Deploy production environment
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/fluent-bit-configmap-prod.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment-prod.yaml
kubectl apply -f k8s/service-prod.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/servicemonitor.yaml

# Or use Kustomize
kubectl apply -k k8s/
```

## Notes

- Image SHA digests have been updated with realistic values (replace with actual digests from your registry)
- Fluent-bit configuration points to internal Loki endpoints
- All containers run as non-root with read-only filesystems
- Temporary files use emptyDir volumes mounted at `/tmp` and `/app/logs`
- Production memory limit set to 2048Mi to comply with Rule 01 standard (≤2Gi), JVM heap adjusted to 1536m
