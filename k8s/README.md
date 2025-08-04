# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the banking platform's k8s standards.

## Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
- CPU requests: 200m, limits: 1000m
- Memory requests: 1536Mi, limits: 3072Mi
- Requests set to ~60% of limits for HPA headroom

### Rule 02 - Pod Security Baseline ✅
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### Rule 03 - Immutable, Trusted Images ✅
- Image pinned with digest: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- No `:latest` tags used
- Internal registry source

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

## Health Checks

- Liveness: `/actuator/health/liveness`
- Readiness: `/actuator/health/readiness`
- Detailed: `/actuator/health/detailed`
