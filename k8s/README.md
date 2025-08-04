# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s-standards-library rules.

## Standards Compliance

### Rule 01 - Resource Limits
- CPU requests: 500m, limits: 2000m
- Memory requests: 1Gi, limits: 2Gi
- Follows 60% request-to-limit ratio for HPA headroom

### Rule 02 - Pod Security Baseline
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance
- Uses pinned image tag with SHA digest
- Registry: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- No `:latest` tags

### Rule 04 - Naming & Labels
- Mandatory labels: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/part-of`, `environment`, `managed-by`
- Release name prefix: `banking-credit-scoring-prod`

### Rule 05 - Logging & Observability
- Prometheus annotations: `prometheus.io/scrape: "true"`, `prometheus.io/port: "8080"`
- Metrics endpoint: `/actuator/prometheus`
- JSON structured logging to stdout

### Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)

## Deployment

```bash
# Apply all manifests
kubectl apply -k k8s/

# Or apply individually
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/networkpolicy.yaml
kubectl apply -f k8s/servicemonitor.yaml
```

## Files

- `namespace.yaml` - Dedicated namespace with proper labels
- `deployment.yaml` - Main application deployment with security context and probes
- `service.yaml` - ClusterIP service with Prometheus annotations
- `configmap.yaml` - ML models configuration
- `networkpolicy.yaml` - Network security policies
- `servicemonitor.yaml` - Prometheus ServiceMonitor for metrics collection
- `kustomization.yaml` - Kustomize configuration for easy deployment
