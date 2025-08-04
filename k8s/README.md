# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that are fully compliant with the k8s-standards-library rules.

## Standards Compliance

### Rule 02 - Security Context Baseline ✅
- `runAsNonRoot: true` - All containers run as non-root user (1001)
- `seccompProfile.type: RuntimeDefault` - Uses runtime default seccomp profile
- `readOnlyRootFilesystem: true` - Root filesystem is read-only
- `capabilities.drop: ["ALL"]` - All Linux capabilities are dropped

### Rule 03 - Image Provenance ✅
- No `:latest` tags used
- Images from trusted registry: `registry.bank.internal`
- SHA256 digest pinning for immutable deployments

### Rule 04 - Naming & Labels ✅
All resources include mandatory labels:
- `app.kubernetes.io/name: credit-scoring-engine`
- `app.kubernetes.io/version: "3.1.0"`
- `app.kubernetes.io/part-of: banking-platform`
- `environment: prod`
- `managed-by: helm`

### Rule 05 - Logging & Observability ✅
- Prometheus metrics exposed on port 8080 at `/actuator/prometheus`
- Prometheus scraping annotations configured
- JSON logging format configured in application.properties

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness`
- Readiness probe: `/actuator/health/readiness`
- Proper timeouts and failure thresholds configured

## Deployment

```bash
# Apply all manifests
kubectl apply -k k8s/

# Or apply individually
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/networkpolicy.yaml
```

## Security Features

- Non-root user execution (UID 1001)
- Read-only root filesystem with writable /tmp volume
- Network policies restricting ingress/egress
- All Linux capabilities dropped
- Seccomp profile enabled

## Monitoring

The application exposes Prometheus metrics at `/actuator/prometheus` and is automatically discovered by Prometheus through service annotations.
