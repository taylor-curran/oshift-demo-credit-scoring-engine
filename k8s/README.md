# Kubernetes Deployment - Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine in compliance with organizational k8s standards (Rules 01-04).

## Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
- **CPU Requests**: 500m (0.5 vCPU)
- **CPU Limits**: 2000m (2 vCPU) 
- **Memory Requests**: 1228Mi (~60% of limit for HPA headroom)
- **Memory Limits**: 2048Mi (reduced from 3072Mi to comply with ≤2Gi limit)

### Rule 02 - Pod Security Baseline ✅
- `runAsNonRoot: true` - Prevents running as root user
- `seccompProfile.type: RuntimeDefault` - Applies runtime's default seccomp profile
- `readOnlyRootFilesystem: true` - Makes root filesystem read-only
- `capabilities.drop: ["ALL"]` - Drops all Linux capabilities
- Writable volumes mounted at `/tmp` and `/models` for application needs

### Rule 03 - Image Provenance ✅
- Uses pinned image tag: `registry.bank.internal/credit-scoring-engine:3.1.0`
- Includes SHA256 digest for immutability
- Sources from approved internal registry (`registry.bank.internal/*`)
- No `:latest` tags used

### Rule 04 - Naming & Label Conventions ✅
- **Release name prefix**: `banking-team-credit-scoring-engine-prod`
- **Mandatory labels**:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: banking-platform`
  - `environment: prod`
  - `managed-by: helm`

## Deployment

### Using kubectl
```bash
kubectl apply -k k8s/
```

### Using kustomize
```bash
kustomize build k8s/ | kubectl apply -f -
```

## Configuration

The application configuration is managed through:
- **ConfigMap**: `banking-team-credit-scoring-engine-config-prod` - Spring Boot properties
- **Environment Variables**: All original Cloud Foundry env vars preserved
- **Service Bindings**: Database and Redis connections via Kubernetes services

## Migration from Cloud Foundry

Key changes from the original `manifest.yml`:
- **Memory**: Reduced from 3072Mi to 2048Mi to comply with Rule 01 (≤2Gi limit)
- **JVM Heap**: Adjusted from 2560m to 1536m to match new memory limit
- **Security**: Added comprehensive security context with non-root execution
- **Health Probes**: Configured liveness and readiness probes for better reliability
- **Labels**: Added all mandatory k8s standard labels for discoverability

## Validation

Run the validation script to verify compliance:
```bash
python3 validate_k8s.py
```
