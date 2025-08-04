# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s standards for the credit scoring engine application.

## Standards Compliance

### Rule 01 - Resource Limits ✅
- CPU requests: 500m, limits: 2000m
- Memory requests: 1800Mi, limits: 3000Mi
- Follows 60% rule of thumb for requests vs limits

### Rule 02 - Pod Security Baseline ✅
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance ✅
- Uses pinned image with SHA digest
- Registry: `registry.bank.internal/*`
- No `:latest` tags

### Rule 04 - Naming & Label Conventions ✅
- Name format: `pe-eng-credit-scoring-engine-dev`
- Required labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: dev`
  - `managed-by: openshift`

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Environment configuration
- `README.md` - This documentation

## Deployment

```bash
kubectl apply -f k8s/
```

## Health Checks

The application provides health checks at `/actuator/health/detailed` endpoint.
