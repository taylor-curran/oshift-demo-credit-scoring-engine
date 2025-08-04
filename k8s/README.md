# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the organization's K8s standards:

## Standards Compliance

### ✅ Rule 01 - Resource Requests & Limits
- All containers have CPU and memory requests and limits defined
- Requests are set to ~60% of limits for HPA headroom
- Memory: 1536Mi requests, 3072Mi limits (matching Cloud Foundry 3GB allocation)
- CPU: 300m requests, 2000m limits

### ✅ Rule 02 - Pod Security Baseline
- `runAsNonRoot: true` enforced at pod and container level
- `seccompProfile.type: RuntimeDefault` configured
- `readOnlyRootFilesystem: true` with writable volumes for /tmp and /models
- All dangerous capabilities dropped with `capabilities.drop: ["ALL"]`

### ✅ Rule 03 - Immutable, Trusted Images
- No `:latest` tags used
- Image pinned to specific version with SHA digest
- Uses trusted internal registry: `registry.bank.internal/*`

### ✅ Rule 04 - Naming & Label Conventions
- Consistent naming: `pe-eng-credit-scoring-engine-prod`
- All mandatory labels present:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: openshift`

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Configuration for ML models
- `secret.yaml` - Placeholder for sensitive data (managed externally)
- `ingress.yaml` - External access via internal banking domains

## Migration from Cloud Foundry

This configuration migrates the application from Cloud Foundry (`manifest.yml`) to Kubernetes while maintaining:
- Same memory allocation (3GB)
- Same replica count (4 instances)
- Same environment variables and configuration
- Same health check endpoints
- Same external routes/domains
