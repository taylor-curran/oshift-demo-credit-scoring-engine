# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine in compliance with k8s standards (Rules 01-06).

## Standards Compliance

### Rule 01 - Resource Requests & Limits
- CPU requests: 500m, limits: 2000m for main container
- Memory requests: 2Gi, limits: 3Gi for main container
- Fluent-bit sidecar: CPU 50m-200m, Memory 128Mi-256Mi

### Rule 02 - Pod Security Baseline
- `runAsNonRoot: true` - Containers run as non-root user
- `seccompProfile.type: RuntimeDefault` - Runtime default seccomp profile
- `readOnlyRootFilesystem: true` - Read-only root filesystem
- `capabilities.drop: ["ALL"]` - All capabilities dropped
- `allowPrivilegeEscalation: false` - Privilege escalation disabled

### Rule 03 - Image Provenance
- Images use pinned tags with SHA digests
- Images from approved registry: `registry.bank.internal/*`
- No `:latest` tags used

### Rule 04 - Naming & Label Conventions
- Release name prefix: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### Rule 05 - Logging & Observability
- Prometheus annotations for metrics scraping:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
  - `prometheus.io/path: "/actuator/prometheus"`
- Fluent-bit sidecar for JSON log collection
- Logs forwarded to Loki stack

### Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness`
- Readiness probe: `/actuator/health/readiness`
- Appropriate timeouts and failure thresholds

## Deployment

Deploy using kustomize:
```bash
kubectl apply -k .
```

Or deploy individual manifests:
```bash
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f fluent-bit-config.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml
```

## Services

The deployment includes:
- Main application container (credit-scoring-engine)
- Fluent-bit sidecar for log shipping
- Service for internal communication
- Ingress for external access
- ConfigMaps for application configuration
