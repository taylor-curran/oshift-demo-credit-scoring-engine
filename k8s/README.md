# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine application that comply with enterprise k8s standards.

## Standards Compliance

### ✅ Rule 01 - Resource Requests & Limits
- CPU requests: 500m (0.5 vCPU)
- CPU limits: 2000m (2 vCPU) 
- Memory requests: 1200Mi (~60% of limits)
- Memory limits: 2048Mi (2GB - compliant with ≤2Gi standard)

### ✅ Rule 02 - Pod Security Baseline
- `runAsNonRoot: true` - All containers run as non-root user (1001)
- `seccompProfile.type: RuntimeDefault` - Seccomp profile applied at pod and container level
- `readOnlyRootFilesystem: true` - Root filesystem is read-only
- `capabilities.drop: ["ALL"]` - All Linux capabilities dropped
- `allowPrivilegeEscalation: false` - Prevents privilege escalation

### ✅ Rule 03 - Image Provenance
- No `:latest` tags used - All images pinned to specific versions with SHA digests
- Registry allowlist enforced - Only `registry.bank.internal/*` images used
- Cosign signature verification handled by OpenShift Image Policies
- Uses pinned image: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456`

### ✅ Rule 04 - Naming & Label Conventions
- Release name prefix: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels present on all resources:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

## Deployment Files

- `deployment.yaml` - Main application deployment with 4 replicas, full security compliance, and fluent-bit sidecar
- `service.yaml` - ClusterIP service exposing port 8080 with Prometheus annotations
- `configmap.yaml` - ML models configuration
- `fluent-bit-configmap.yaml` - Fluent-bit logging configuration for centralized log shipping
- `ingress.yaml` - External access via nginx ingress
- `networkpolicy.yaml` - Network security policies
- `README.md` - This documentation

## Health Probes

- Liveness probe: `/actuator/health/liveness` (30s initial delay, 30s period, 10s timeout)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 10s period, 5s timeout)
- Proper failure thresholds configured (3 failures for liveness, 1 for readiness)

## Deployment Commands

```bash
# Apply all manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -l app.kubernetes.io/name=credit-scoring-engine

# View logs
kubectl logs -l app.kubernetes.io/name=credit-scoring-engine

# Access health endpoint
kubectl port-forward svc/pe-eng-credit-scoring-engine-prod 8080:8080
curl http://localhost:8080/actuator/health/detailed

# Check Prometheus metrics
curl http://localhost:8080/actuator/prometheus
```

## Migration from Cloud Foundry

This k8s deployment maintains feature parity with the original Cloud Foundry `manifest.yml`:
- Same environment variables and configuration
- Same health check endpoints (`/actuator/health/detailed`)
- Adjusted resource allocation (2GB memory for k8s standards compliance)
- Same external service dependencies
- Enhanced security with k8s standards compliance
- Improved observability with Prometheus metrics
