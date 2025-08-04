# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s-standards-library rules.

## Standards Compliance

### Rule 02 - Security Context Baseline
- ✅ `runAsNonRoot: true` - All containers run as non-root user (1001)
- ✅ `seccompProfile.type: RuntimeDefault` - Runtime default seccomp profile applied
- ✅ `readOnlyRootFilesystem: true` - Root filesystem is read-only
- ✅ `capabilities.drop: ["ALL"]` - All Linux capabilities dropped
- ✅ `allowPrivilegeEscalation: false` - Privilege escalation disabled

### Rule 03 - Image Provenance
- ✅ Tag pinning - Uses specific version tag `3.1.0` instead of `:latest`
- ✅ Registry allow-list - Uses `registry.bank.internal` trusted registry
- ✅ Ready for Cosign signature verification via OpenShift Image Policies

### Rule 04 - Naming & Label Conventions
- ✅ Mandatory labels applied:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: banking-platform`
  - `environment: production`
  - `managed-by: kubernetes`
- ✅ Consistent naming across all resources

### Rule 05 - Logging & Observability
- ✅ Prometheus annotations for metrics scraping:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
  - `prometheus.io/path: "/actuator/prometheus"`
- ✅ Spring Boot Actuator endpoints exposed for monitoring
- ✅ JSON logging via Spring Boot default configuration

### Rule 06 - Health Probes
- ✅ Liveness probe: `/actuator/health/liveness`
- ✅ Readiness probe: `/actuator/health/readiness`
- ✅ Proper timeouts and failure thresholds configured

## Deployment

```bash
# Apply all manifests
kubectl apply -k k8s/

# Or apply individually
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/ingress.yaml
```

## Resource Requirements

- **CPU**: 500m requests, 2000m limits
- **Memory**: 2Gi requests, 3Gi limits
- **Replicas**: 4 (matching Cloud Foundry configuration)

## Security Features

- Non-root user execution (UID 1001)
- Read-only root filesystem with writable `/tmp` volume
- Dropped Linux capabilities
- Runtime default seccomp profile
- TLS-enabled ingress with SSL redirect
