# Kubernetes Deployment

This directory contains Kubernetes manifests for the Credit Scoring Engine that comply with the k8s standards (Rules 01-06).

## Standards Compliance

### Rule 01 - Resource Limits
- ✅ CPU requests: 1000m, limits: 2000m
- ✅ Memory requests: 1536Mi, limits: 3072Mi
- ✅ Requests set to ~75% of limits for HPA headroom

### Rule 02 - Security Context
- ✅ `runAsNonRoot: true`
- ✅ `seccompProfile.type: RuntimeDefault`
- ✅ `readOnlyRootFilesystem: true`
- ✅ `capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance
- ✅ Pinned image tag with SHA digest
- ✅ Uses approved registry: `registry.bank.internal`
- ✅ No `:latest` tags

### Rule 04 - Naming & Labels
- ✅ Mandatory labels: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/part-of`, `environment`, `managed-by`
- ✅ Release name prefix: `credit-scoring-engine-prod`

### Rule 05 - Logging & Observability
- ✅ Prometheus annotations: `prometheus.io/scrape: "true"`, `prometheus.io/port: "8080"`
- ✅ JSON logging configuration in ConfigMap
- ✅ Metrics endpoint exposed on port 8080

### Rule 06 - Health Probes
- ✅ Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- ✅ Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)

## Deployment

### Using kubectl
```bash
kubectl apply -k k8s/
```

### Using kustomize
```bash
kustomize build k8s/ | kubectl apply -f -
```

## Files

- `deployment.yaml` - Main application deployment
- `service.yaml` - Service definition with Prometheus annotations
- `configmap.yaml` - Application configuration with JSON logging
- `kustomization.yaml` - Kustomize configuration for environment management
- `README.md` - This documentation
