# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the banking organization's k8s standards.

## Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
- CPU requests: 200m, limits: 2000m
- Memory requests: 1536Mi, limits: 3072Mi
- Follows 60% request-to-limit ratio for HPA headroom

### Rule 02 - Pod Security Baseline ✅
- `runAsNonRoot: true`
- `runAsUser: 1001` (non-root user)
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`
- `seccompProfile.type: RuntimeDefault`

### Rule 03 - Immutable, Trusted Images ✅
- Uses pinned image with SHA digest
- Registry: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
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
kubectl apply -f k8s/
```

## Files

- `namespace.yaml` - Dedicated namespace for credit scoring
- `configmap.yaml` - Application configuration
- `deployment.yaml` - Main application deployment
- `service.yaml` - ClusterIP service
- `networkpolicy.yaml` - Network security policies
- `hpa.yaml` - Horizontal Pod Autoscaler
- `poddisruptionbudget.yaml` - High availability protection
