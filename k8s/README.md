# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the banking platform's k8s standards.

## Standards Compliance

All manifests in this directory comply with the following standards:

### Rule 01 - Resource Requests & Limits
- CPU requests: 600m (60% of 1000m limit)
- Memory requests: 1843Mi (60% of 3072Mi limit)
- Prevents noisy-neighbor issues in multi-tenant clusters

### Rule 02 - Pod Security Baseline
- `runAsNonRoot: true` - No root user execution
- `seccompProfile.type: RuntimeDefault` - Secure computing profile
- `readOnlyRootFilesystem: true` - Immutable filesystem
- `capabilities.drop: ["ALL"]` - Minimal capabilities

### Rule 03 - Immutable, Trusted Images
- Uses pinned image with SHA digest from approved registry
- Registry: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- No `:latest` tags allowed

### Rule 04 - Naming & Label Conventions
- Consistent naming: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: openshift`

### Rule 05 - Logging & Observability
- Prometheus scraping annotations
- JSON structured logging to stdout
- Metrics endpoint at `/metrics`

### Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness` (30s delay, 3 failures)
- Readiness probe: `/actuator/health/readiness` (10s delay, 1 failure)

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Application configuration
- `route.yaml` - OpenShift routes for internal and API access
- `README.md` - This documentation

## Deployment

```bash
kubectl apply -f k8s/
```

## Verification

```bash
# Check deployment status
kubectl get deployment pe-eng-credit-scoring-engine-prod

# Check pod security compliance
kubectl describe pod -l app.kubernetes.io/name=credit-scoring-engine

# Verify resource limits
kubectl describe pod -l app.kubernetes.io/name=credit-scoring-engine | grep -A 10 "Limits\|Requests"

# Test health endpoints
kubectl port-forward svc/pe-eng-credit-scoring-engine-prod 8080:8080
curl http://localhost:8080/actuator/health/liveness
curl http://localhost:8080/actuator/health/readiness
```
