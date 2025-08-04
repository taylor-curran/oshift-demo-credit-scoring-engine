# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s standards library rules.

## Standards Compliance

### Rule 02 - Security Context Baseline
- ✅ `runAsNonRoot: true`
- ✅ `seccompProfile.type: RuntimeDefault`
- ✅ `readOnlyRootFilesystem: true`
- ✅ `capabilities.drop: ["ALL"]`

### Rule 01 - Resource Requests & Limits
- ✅ CPU requests: `1200m` (1.2 vCPU)
- ✅ CPU limits: `2000m` (2 vCPU) 
- ✅ Memory requests: `1843Mi` (~1.8 GB)
- ✅ Memory limits: `3072Mi` (3 GB)
- ✅ Requests ≈ 60% of limits for HPA headroom

### Rule 03 - Image Provenance
- ✅ Pinned image tag: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730`
- ✅ Approved registry: `registry.bank.internal/*`
- ✅ Cosign signature verification (handled by OpenShift Image Policies)

### Rule 04 - Naming & Label Conventions
- ✅ Release-name prefix: `pe-eng-credit-scoring-engine-prod` (follows `<team>-<app>-<env>` pattern)
- ✅ Mandatory labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### Rule 05 - Logging & Observability
- ✅ Prometheus annotations:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`

### Rule 06 - Health Probes
- ✅ Liveness probe: `/actuator/health/liveness` (30s initial delay, 10s period)
- ✅ Readiness probe: `/actuator/health/readiness` (10s initial delay, 5s period)
- ✅ Startup probe: `/actuator/health/readiness` (15s initial delay, 10s period, 30 failures max)

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Configuration for ML models
- `secret.yaml` - Secrets for database and API keys
- `ingress.yaml` - Ingress for external access
- `kustomization.yaml` - Kustomize configuration

## Deployment

```bash
kubectl apply -k k8s/
```

## Verification

```bash
# Check deployment status
kubectl get deployment pe-eng-credit-scoring-engine-prod

# Check pod security context
kubectl describe pod -l app.kubernetes.io/name=credit-scoring-engine

# Verify health endpoints
kubectl port-forward svc/pe-eng-credit-scoring-engine-service 8080:8080
curl http://localhost:8080/actuator/health/liveness
curl http://localhost:8080/actuator/health/readiness
```
