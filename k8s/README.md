# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine application, migrated from Cloud Foundry and compliant with organizational k8s standards.

## Standards Compliance

This deployment follows all four mandatory k8s standards:

### Rule 01 - Resource Requests & Limits ✅
- **CPU requests**: 500m (0.5 vCPU) 
- **CPU limits**: 2000m (2 vCPU)
- **Memory requests**: 1536Mi (~1.5 GB)
- **Memory limits**: 3072Mi (3 GB)
- Requests set to ~75% of limits for HPA headroom

### Rule 02 - Pod Security Baseline ✅
- `runAsNonRoot: true` - Application runs as non-root user
- `seccompProfile.type: RuntimeDefault` - Secure computing profile enabled
- `readOnlyRootFilesystem: true` - Filesystem is read-only
- `capabilities.drop: ["ALL"]` - All dangerous capabilities dropped
- Writable volumes mounted only where needed (/tmp, /models)

### Rule 03 - Immutable, Trusted Images ✅
- Image tagged with specific version: `3.1.0`
- SHA256 digest pinning for immutability
- Registry from approved allow-list: `registry.bank.internal/*`
- No `:latest` tags used

### Rule 04 - Naming & Label Conventions ✅
- **Release name**: `pe-eng-credit-scoring-engine-prod`
- **Mandatory labels**:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

## Deployment Files

- `namespace.yaml` - Dedicated namespace for isolation
- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service for internal communication
- `configmap.yaml` - Configuration data and ML models
- `secrets.yaml` - Sensitive data (passwords, API keys, TLS certs)
- `ingress.yaml` - External access routing

## Migration from Cloud Foundry

This deployment preserves all functionality from the original `manifest.yml`:

- **Scaling**: 4 application instances → 4 Kubernetes replicas
- **Memory**: 3072M allocation maintained
- **Environment variables**: All CF env vars migrated to k8s env
- **Health checks**: CF health endpoint → k8s liveness/readiness probes
- **Routing**: CF routes → Kubernetes ingress rules
- **Services**: CF services → Kubernetes secrets and external service references

## Deployment Instructions

```bash
# Apply in order
kubectl apply -f namespace.yaml
kubectl apply -f secrets.yaml
kubectl apply -f configmap.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml
```

## Security Notes

- All secrets contain placeholder values and must be updated with production data
- TLS certificates need to be provided for ingress
- Database and Redis connection details should be configured via secrets
- API keys for external services (Experian, Equifax, etc.) must be securely managed
