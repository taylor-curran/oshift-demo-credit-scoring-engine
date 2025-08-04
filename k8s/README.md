# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with enterprise k8s standards for the Credit Scoring Engine application.

## Standards Compliance

### ✅ Rule 01 - Resource Requests & Limits
- **CPU requests**: 500m (0.5 vCPU) per pod
- **CPU limits**: 2000m (2 vCPU) per pod  
- **Memory requests**: 1536Mi per pod
- **Memory limits**: 3072Mi per pod
- **Request/Limit ratio**: ~60% for optimal HPA headroom

### ✅ Rule 02 - Pod Security Baseline
- **runAsNonRoot**: `true` (UID 1001)
- **readOnlyRootFilesystem**: `true`
- **seccompProfile**: `RuntimeDefault`
- **capabilities**: All dropped (`["ALL"]`)
- **allowPrivilegeEscalation**: `false`

### ✅ Rule 03 - Immutable, Trusted Images
- **Image**: `registry.bank.internal/credit-scoring-engine:3.1.0`
- **Registry**: Internal bank registry (compliant)
- **Tag**: Pinned version (no `:latest`)
- **Signature**: Ready for Cosign verification

### ✅ Rule 04 - Naming & Label Conventions
- **Release name**: `pe-eng-credit-scoring-engine-prod`
- **Mandatory labels**:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

## Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/

# Verify deployment
kubectl get pods -n credit-scoring-engine
kubectl get svc -n credit-scoring-engine
```

## Architecture

- **Namespace**: `credit-scoring-engine`
- **Replicas**: 4 (with HPA scaling 4-12)
- **Ingress**: Two routes for internal and external access
- **Network Policy**: Restricted ingress/egress for security
- **Health Checks**: Liveness and readiness probes configured
- **Volumes**: Read-only root filesystem with writable `/tmp` and model storage

## Migration from Cloud Foundry

This Kubernetes deployment maintains feature parity with the original Cloud Foundry `manifest.yml`:
- Same memory allocation (3GB)
- Same replica count (4 instances)
- All environment variables preserved
- Health check endpoints maintained
- Multi-route ingress configuration
