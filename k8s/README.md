# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with enterprise k8s standards for the Credit Scoring Engine application.

## Standards Compliance

### ✅ Rule 01 - Resource Limits & Requests
- CPU requests: 1200m, limits: 2000m (60% ratio)
- Memory requests: 1536Mi, limits: 3072Mi (50% ratio)
- Follows recommended request-to-limit ratio for HPA headroom

### ✅ Rule 02 - Pod Security Baseline
- `runAsNonRoot: true` with user ID 1001
- `readOnlyRootFilesystem: true` with writable tmp volumes
- `seccompProfile.type: RuntimeDefault`
- `capabilities.drop: ["ALL"]`

### ✅ Rule 03 - Immutable, Trusted Images
- Pinned image with SHA256 digest (no `:latest` tags)
- Uses approved registry: `registry.bank.internal/*`
- Image: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730`

### ✅ Rule 04 - Naming & Label Conventions
- Release name: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

## Deployment Files

- `namespace.yaml` - Dedicated namespace with proper labels
- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service for internal communication
- `configmap.yaml` - ML model configuration
- `ingress.yaml` - External access routing
- `README.md` - This documentation

## Deployment Commands

```bash
# Apply all manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n credit-scoring

# View logs
kubectl logs -f deployment/pe-eng-credit-scoring-engine-prod -n credit-scoring
```

## Migration from Cloud Foundry

This Kubernetes deployment maintains feature parity with the original Cloud Foundry manifest.yml:
- 4 application instances → 4 pod replicas
- 3GB memory allocation → 3072Mi memory limit
- Health check endpoint → liveness/readiness probes
- Environment variables → preserved in deployment spec
- External routes → ingress configuration
