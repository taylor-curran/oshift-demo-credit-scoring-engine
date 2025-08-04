# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s standards library rules:

## Standards Compliance

### Rule 02 - Security Context Baseline ✅
- `runAsNonRoot: true` - All containers run as non-root user
- `seccompProfile.type: RuntimeDefault` - Uses runtime default seccomp profile
- `readOnlyRootFilesystem: true` - Root filesystem is read-only
- `capabilities.drop: ["ALL"]` - All Linux capabilities are dropped
- `allowPrivilegeEscalation: false` - Prevents privilege escalation

### Rule 03 - Image Provenance ✅
- No `:latest` tags used - Image uses pinned version `3.1.0` with SHA digest
- Uses approved registry: `registry.bank.internal/credit-scoring-engine`
- Image includes SHA256 digest for immutability

### Rule 04 - Naming & Label Conventions ✅
- **Mandatory labels applied to all resources:**
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: banking-platform`
  - `environment: prod`
  - `managed-by: helm`
- **Release name prefix:** `credit-scoring-engine-prod`

### Rule 05 - Logging & Observability ✅
- Prometheus annotations for metrics scraping:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
  - `prometheus.io/path: "/actuator/prometheus"`

### Rule 06 - Health Probes ✅
- **Liveness probe:** `/actuator/health/liveness` on port 8081
- **Readiness probe:** `/actuator/health/readiness` on port 8081
- Proper timeouts and failure thresholds configured

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing ports 8080 and 8081
- `configmap.yaml` - Configuration for ML models
- `ingress.yaml` - Ingress for external access with TLS
- `networkpolicy.yaml` - Network security policies

## Deployment

```bash
kubectl apply -f k8s/
```

## Verification

```bash
# Check deployment status
kubectl get deployment credit-scoring-engine-prod

# Verify security context
kubectl describe pod -l app.kubernetes.io/name=credit-scoring-engine

# Check service endpoints
kubectl get svc credit-scoring-engine-service
```
