# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that are fully compliant with k8s standards Rules 01-06.

## Standards Compliance

### Rule 01 - Resource Limits
- ✅ CPU requests: 500m, limits: 2000m
- ✅ Memory requests: 1536Mi, limits: 2Gi

### Rule 02 - Pod Security Baseline
- ✅ `runAsNonRoot: true`
- ✅ `seccompProfile.type: RuntimeDefault`
- ✅ `readOnlyRootFilesystem: true`
- ✅ `capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance
- ✅ No `:latest` tags - using pinned version `3.1.0`
- ✅ SHA digest for immutable image reference
- ✅ Registry allowlist - using `registry.bank.internal`

### Rule 04 - Naming & Labels
- ✅ Mandatory labels: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/part-of`, `environment`, `managed-by`
- ✅ Release name prefix: `pe-eng-credit-scoring-engine-prod`

### Rule 05 - Logging & Observability
- ✅ JSON structured logging configured
- ✅ Prometheus annotations: `prometheus.io/scrape`, `prometheus.io/port`, `prometheus.io/path`

### Rule 06 - Health Probes
- ✅ Liveness probe: `/actuator/health/liveness`
- ✅ Readiness probe: `/actuator/health/readiness`

## Deployment

```bash
kubectl apply -f k8s/
```

## Files

- `namespace.yaml` - Creates the credit-scoring namespace
- `deployment.yaml` - Main application deployment
- `service.yaml` - ClusterIP service with Prometheus annotations
- `serviceaccount.yaml` - Service account with minimal permissions
- `configmap.yaml` - Application configuration
- `ingress.yaml` - HTTPS ingress with TLS termination
