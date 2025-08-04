# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine application that comply with organizational k8s standards.

## Standards Compliance

These manifests comply with the following k8s standards:

### Rule 01 - Resource Limits
- ✅ CPU requests: 1000m, limits: 2000m
- ✅ Memory requests: 1800Mi, limits: 3072Mi
- ✅ Requests set to ~60% of limits for HPA headroom

### Rule 02 - Pod Security Baseline
- ✅ `runAsNonRoot: true`
- ✅ `seccompProfile.type: RuntimeDefault`
- ✅ `readOnlyRootFilesystem: true`
- ✅ `capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance
- ✅ Pinned image tag: `registry.bank.internal/credit-scoring-engine:3.1.0`
- ✅ Uses approved internal registry
- ✅ No `:latest` tags

### Rule 04 - Naming & Labels
- ✅ Mandatory labels: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/part-of`, `environment`, `managed-by`
- ✅ Consistent naming convention

### Rule 05 - Logging & Observability
- ✅ Prometheus annotations: `prometheus.io/scrape: "true"`, `prometheus.io/port: "8080"`
- ✅ Metrics exposed on port 8080

### Rule 06 - Health Probes
- ✅ Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- ✅ Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Application configuration

## Deployment

```bash
kubectl apply -f k8s/
```

## Monitoring

The application exposes Prometheus metrics at `/metrics` on port 8080 and will automatically be discovered by Prometheus due to the annotations.

Health checks are available at:
- `/actuator/health/liveness` - Liveness probe
- `/actuator/health/readiness` - Readiness probe
- `/actuator/health/detailed` - Detailed health information
