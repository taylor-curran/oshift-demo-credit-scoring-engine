# Kubernetes Manifests - K8s Standards Compliant

This directory contains Kubernetes deployment manifests for the Credit Scoring Engine that comply with all k8s standards (Rules 01-06).

## Standards Compliance

### ✅ Rule 01 - Resource Requests & Limits
- **CPU requests**: 500m (0.5 vCPU)
- **Memory requests**: 1536Mi (1.5 GB)
- **CPU limits**: 2000m (2 vCPU)
- **Memory limits**: 3072Mi (3 GB)
- Requests are ~75% of limits for HPA headroom

### ✅ Rule 02 - Pod Security Baseline
- `runAsNonRoot: true` - No root user execution
- `seccompProfile.type: RuntimeDefault` - Secure system call filtering
- `readOnlyRootFilesystem: true` - Immutable root filesystem
- `capabilities.drop: ["ALL"]` - All dangerous capabilities dropped
- `allowPrivilegeEscalation: false` - No privilege escalation

### ✅ Rule 03 - Image Provenance
- Image uses pinned tag: `registry.bank.internal/credit-scoring-engine:3.1.0`
- No `:latest` tags used
- Uses approved internal registry: `registry.bank.internal/*`
- Production images must be Cosign signed (enforced by OpenShift Image Policies)

### ✅ Rule 04 - Naming & Label Conventions
- **Release name**: `credit-scoring-engine-prod` (follows `<app>-<env>` pattern)
- **Mandatory labels**:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: kubernetes`

### ✅ Rule 05 - Logging & Observability
- **Prometheus annotations**:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
- Application configured to emit JSON logs to stdout
- Metrics endpoint available at `/metrics` on port 8080
- Ready for fluent-bit sidecar integration with OpenShift Loki stack

### ✅ Rule 06 - Health Probes
- **Liveness probe**: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- **Readiness probe**: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)
- Uses Spring Boot Actuator endpoints for JVM health monitoring

## Deployment

```bash
# Apply all manifests
kubectl apply -k k8s/

# Or apply individually
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## Migration from Cloud Foundry

This replaces the Cloud Foundry `manifest.yml` configuration with Kubernetes-native manifests that maintain the same functionality while adding security and observability improvements required by the k8s standards.

Key differences:
- Added security context with non-root execution
- Added resource limits and requests
- Added health probes for better reliability
- Added Prometheus monitoring annotations
- Uses read-only root filesystem with temporary volumes
