# Kubernetes Manifests - Standards Compliance

This directory contains Kubernetes manifests for the Credit Scoring Engine application that comply with the banking k8s standards.

## Standards Compliance

### ✅ Rule 01 - Resource Requests & Limits
- All containers have CPU and memory requests and limits defined
- Requests set to ~60% of limits for HPA headroom
- CPU: 500m request, 2000m limit
- Memory: 1536Mi request, 3072Mi limit

### ✅ Rule 02 - Pod Security Baseline
- `runAsNonRoot: true` - pods run as non-root user (1001)
- `seccompProfile.type: RuntimeDefault` - secure computing profile
- `readOnlyRootFilesystem: true` - immutable root filesystem
- `capabilities.drop: ["ALL"]` - all dangerous capabilities dropped
- `allowPrivilegeEscalation: false` - prevents privilege escalation

### ✅ Rule 03 - Image Provenance
- No `:latest` tags used
- Pinned image with SHA256 digest: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- Uses approved internal registry: `registry.bank.internal`

### ✅ Rule 04 - Naming & Label Conventions
- Release name follows pattern: `pe-eng-credit-scoring-engine-prod`
- All mandatory labels present:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### ✅ Rule 05 - Observability
- Prometheus metrics endpoint configured: `/actuator/prometheus`
- ServiceMonitor for Prometheus scraping
- Proper health check endpoints: `/actuator/health/liveness` and `/actuator/health/readiness`
- JSON logging enabled via Spring Boot Actuator

## Deployment Files

- `namespace.yaml` - Dedicated namespace with proper labels
- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service for internal communication
- `configmap.yaml` - Configuration for ML models
- `hpa.yaml` - Horizontal Pod Autoscaler (4-12 replicas)
- `servicemonitor.yaml` - Prometheus monitoring configuration
- `networkpolicy.yaml` - Network security policies

## Migration from Cloud Foundry

This replaces the Cloud Foundry `manifest.yml` with proper Kubernetes resources while maintaining the same application configuration and scaling characteristics.

## Deployment

```bash
kubectl apply -f k8s/
```

Note: Ensure the image `registry.bank.internal/credit-scoring-engine:3.1.0` is built and pushed to the internal registry before deployment.
