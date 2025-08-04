# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests for the Credit Scoring Engine application, fully compliant with k8s standards (Rules 02-06).

## Standards Compliance

### Rule 02 - Pod Security Baseline ✅
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### Rule 03 - Immutable, Trusted Images ✅
- Uses trusted registry: `registry.bank.internal`
- Pinned version tag: `3.1.0`
- SHA digest for immutability
- No `:latest` tags

### Rule 04 - Naming & Label Conventions ✅
- Mandatory labels: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/part-of`, `environment`, `managed-by`
- Release name prefix: `pe-eng-credit-scoring-engine-prod`

### Rule 05 - Logging & Observability ✅
- Prometheus annotations: `prometheus.io/scrape: "true"`, `prometheus.io/port: "8080"`
- JSON structured logging
- Health endpoints exposed

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness`
- Readiness probe: `/actuator/health/readiness`
- Startup probe: `/actuator/health`

## Deployment

```bash
kubectl apply -k .
```

## Files

- `deployment.yaml` - Main application deployment
- `service.yaml` - Service definition
- `configmap.yaml` - Application configuration
- `ml-models-configmap.yaml` - ML model configuration
- `ingress.yaml` - Ingress routing
- `networkpolicy.yaml` - Network security policies
- `kustomization.yaml` - Kustomize configuration
