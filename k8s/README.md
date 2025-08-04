# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with enterprise K8s standards for the Credit Scoring Engine application.

## Standards Compliance

### ✅ Rule 01 - Resource Requests & Limits
- **CPU requests**: 500m (0.5 vCPU)
- **CPU limits**: 2000m (2 vCPU) 
- **Memory requests**: 1536Mi (~60% of limits for HPA headroom)
- **Memory limits**: 3072Mi (3GB as per original manifest)

### ✅ Rule 02 - Pod Security Baseline
- **runAsNonRoot**: true
- **runAsUser/runAsGroup**: 1001 (non-root)
- **readOnlyRootFilesystem**: true
- **seccompProfile**: RuntimeDefault
- **capabilities.drop**: ["ALL"]
- **allowPrivilegeEscalation**: false

### ✅ Rule 03 - Immutable, Trusted Images
- **No :latest tags**: Uses pinned version `3.1.0` with SHA256 digest
- **Registry allowlist**: Uses `registry.bank.internal/*` (approved internal registry)
- **Cosign signature**: Production images must have valid signatures (handled by OpenShift Image Policies)

### ✅ Rule 04 - Naming & Label Conventions
- **Release name**: `pe-eng-credit-scoring-engine-prod` (team-app-env format)
- **Mandatory labels**:
  - `app.kubernetes.io/name`: credit-scoring-engine
  - `app.kubernetes.io/version`: 3.1.0
  - `app.kubernetes.io/part-of`: retail-banking
  - `environment`: prod
  - `managed-by`: helm

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Configuration for ML models
- `ingress.yaml` - External access via internal banking domains

## Deployment

```bash
kubectl apply -f k8s/
```

## Health Checks

- **Liveness probe**: `/actuator/health` (60s initial delay)
- **Readiness probe**: `/actuator/health/detailed` (30s initial delay)

## Security Features

- Read-only root filesystem with writable `/tmp` volume
- Non-root user execution (UID 1001)
- All Linux capabilities dropped
- Seccomp profile enabled
