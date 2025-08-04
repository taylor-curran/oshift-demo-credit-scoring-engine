# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the bank's k8s standards (Rules 01-06).

## Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
- CPU requests: 500m, limits: 2000m
- Memory requests: 2Gi, limits: 3Gi
- Follows 60% request-to-limit ratio for HPA headroom

### Rule 02 - Pod Security Baseline ✅
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### Rule 03 - Immutable, Trusted Images ✅
- Uses pinned image with SHA digest: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- Registry: `registry.bank.internal/*` (approved)
- No `:latest` tags

### Rule 04 - Naming & Label Conventions ✅
- Release name: `pe-eng-credit-scoring-engine-prod`
- Required labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### Rule 05 - Logging & Observability ✅
- Prometheus annotations:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
  - `prometheus.io/path: "/actuator/prometheus"`
- JSON structured logging via Spring Boot Actuator

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness`
- Readiness probe: `/actuator/health/readiness`
- Startup probe configured for JVM applications

## Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/

# Or apply individually
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/networkpolicy.yaml
```

## Files

- `namespace.yaml` - Creates credit-scoring namespace
- `configmap.yaml` - Application configuration with all environment variables
- `deployment.yaml` - Main application deployment with security contexts
- `service.yaml` - ClusterIP service with Prometheus annotations
- `ingress.yaml` - External access configuration for banking domains
- `networkpolicy.yaml` - Network security policies
- `fluent-bit-config.yaml` - Logging configuration
- `fluent-bit-sidecar.yaml` - Log collection sidecar

## Migration from Cloud Foundry

This replaces the `manifest.yml` Cloud Foundry configuration with standards-compliant Kubernetes manifests.

Key changes:
- Migrated from CF buildpacks to containerized deployment
- Added security contexts and resource constraints
- Implemented proper labeling and naming conventions
- Added horizontal pod autoscaling
- Configured ingress for external access
- Added network policies for security
- Integrated observability and logging
