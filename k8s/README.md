# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s standards library rules.

## Standards Compliance

### Rule 02 - Security Context Baseline
- ✅ `runAsNonRoot: true`
- ✅ `seccompProfile.type: RuntimeDefault`
- ✅ `readOnlyRootFilesystem: true`
- ✅ `capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance
- ✅ Pinned image tag: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- ✅ Approved registry: `registry.bank.internal/*`
- ✅ Cosign signature verification (handled by OpenShift Image Policies)

### Rule 04 - Naming & Label Conventions
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
- ✅ Liveness probe: `/actuator/health/liveness`
- ✅ Readiness probe: `/actuator/health/readiness`

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
kubectl get deployment credit-scoring-engine-prod

# Check pod security context
kubectl describe pod -l app.kubernetes.io/name=credit-scoring-engine

# Verify health endpoints
kubectl port-forward svc/credit-scoring-engine-service 8080:8080
curl http://localhost:8080/actuator/health/liveness
curl http://localhost:8080/actuator/health/readiness
```
