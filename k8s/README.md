# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the bank's k8s standards (Rules 01-04).

## Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
- CPU requests: 300m, limits: 2000m
- Memory requests: 1536Mi, limits: 3072Mi
- Follows 60% request-to-limit ratio for HPA headroom

### Rule 02 - Pod Security Baseline ✅
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### Rule 03 - Immutable, Trusted Images ✅
- Uses pinned image with SHA digest
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

## Deployment

```bash
# Apply all manifests
kubectl apply -k k8s/

# Or apply individually
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/ingress.yaml
kubectl apply -f k8s/hpa.yaml
```

## Migration from Cloud Foundry

This replaces the `manifest.yml` Cloud Foundry configuration with standards-compliant Kubernetes manifests.

Key changes:
- Migrated from CF buildpacks to containerized deployment
- Added security contexts and resource constraints
- Implemented proper labeling and naming conventions
- Added horizontal pod autoscaling
- Configured ingress for external access
