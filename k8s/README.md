# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine application with full compliance to k8s standards (Rules 01-06).

## Standards Compliance

### Rule 01 - Resource Limits
- ✅ CPU requests: 500m, limits: 2000m
- ✅ Memory requests: 1536Mi, limits: 2Gi
- ✅ Fluent-bit sidecar: CPU 50m-100m, Memory 64Mi-128Mi

### Rule 02 - Security Context
- ✅ runAsNonRoot: true
- ✅ seccompProfile.type: RuntimeDefault
- ✅ readOnlyRootFilesystem: true
- ✅ capabilities.drop: ["ALL"]

### Rule 03 - Image Provenance
- ✅ Pinned images with SHA256 digests
- ✅ Registry allow-list: registry.bank.internal/*
- ✅ No :latest tags

### Rule 04 - Naming & Labels
- ✅ Mandatory labels: app.kubernetes.io/name, version, part-of, environment, managed-by
- ✅ Release-name prefix: pe-eng-credit-scoring-engine-prod

### Rule 05 - Logging & Observability
- ✅ JSON structured logging configuration
- ✅ Fluent-bit sidecar for log shipping
- ✅ Prometheus annotations: scrape, port, path

### Rule 06 - Health Probes
- ✅ Liveness probe: /actuator/health/liveness (30s delay, 3 failures)
- ✅ Readiness probe: /actuator/health/readiness (10s delay, 1 failure)

## Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n credit-scoring -l app.kubernetes.io/name=credit-scoring-engine

# View logs
kubectl logs -n credit-scoring -l app.kubernetes.io/name=credit-scoring-engine -c credit-scoring-engine

# Check fluent-bit sidecar
kubectl logs -n credit-scoring -l app.kubernetes.io/name=credit-scoring-engine -c fluent-bit
```

## Files

- `namespace.yaml` - Credit scoring namespace
- `deployment.yaml` - Main application deployment with fluent-bit sidecar
- `service.yaml` - ClusterIP service with Prometheus annotations
- `serviceaccount.yaml` - Service account with minimal permissions
- `configmap.yaml` - Application configuration
- `fluent-bit-configmap.yaml` - Fluent-bit logging configuration
- `ingress.yaml` - Ingress for external access
