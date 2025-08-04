# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s standards (Rules 01-06) for the Credit Scoring Engine application.

## Standards Compliance

### Rule 01 - Resource Limits
- ✅ CPU requests: 500m, limits: 2000m
- ✅ Memory requests: 1536Mi, limits: 3072Mi
- ✅ Requests ≈ 60% of limits for HPA headroom

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
- ✅ Release-name prefix: `retail-banking-credit-scoring-engine-prod`

### Rule 05 - Logging & Observability
- ✅ Prometheus annotations: `prometheus.io/scrape: "true"`, `prometheus.io/port: "8080"`
- ✅ Metrics exposed on port 8080
- ✅ JSON logging to stdout (configured via Spring Boot)

### Rule 06 - Health Probes
- ✅ Liveness probe: `/actuator/health/liveness` with 30s initial delay
- ✅ Readiness probe: `/actuator/health/readiness` with 10s initial delay

## Deployment

```bash
kubectl apply -f k8s/
```

## Files

- `namespace.yaml` - Dedicated namespace for the application
- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service for internal communication
- `configmap.yaml` - Configuration for ML models
- `ingress.yaml` - External access configuration
