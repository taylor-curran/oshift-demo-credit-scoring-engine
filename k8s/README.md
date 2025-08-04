# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine application that comply with enterprise k8s standards.

## Standards Compliance

### ✅ Rule 01 - Resource Requests & Limits
- CPU requests: 500m (0.5 vCPU)
- CPU limits: 2000m (2 vCPU) 
- Memory requests: 1536Mi (~60% of limits)
- Memory limits: 3072Mi (3GB as per original manifest)

### ✅ Rule 02 - Pod Security Baseline
- `runAsNonRoot: true` - Prevents root execution
- `seccompProfile.type: RuntimeDefault` - Applies secure computing profile
- `readOnlyRootFilesystem: true` - Locks filesystem
- `capabilities.drop: ["ALL"]` - Drops dangerous capabilities

### ✅ Rule 03 - Immutable, Trusted Images
- Uses pinned image with SHA digest: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- No `:latest` tags
- Images from approved internal registry

### ✅ Rule 04 - Naming & Label Conventions
- Release name: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels applied:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

## Deployment Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 80
- `configmap.yaml` - ML models configuration
- `ingress.yaml` - External access via nginx ingress
- `README.md` - This documentation

## Deployment Commands

```bash
# Apply all manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -l app.kubernetes.io/name=credit-scoring-engine

# View logs
kubectl logs -l app.kubernetes.io/name=credit-scoring-engine

# Access health endpoint
kubectl port-forward svc/pe-eng-credit-scoring-engine-prod 8080:80
curl http://localhost:8080/actuator/health/detailed
```

## Migration from Cloud Foundry

This k8s deployment maintains feature parity with the original Cloud Foundry `manifest.yml`:
- Same environment variables and configuration
- Same health check endpoints
- Same resource allocation (3GB memory)
- Same external service dependencies
- Same routing configuration via ingress
