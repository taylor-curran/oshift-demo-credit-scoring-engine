# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s-standards-library rules.

## Standards Compliance

### Rule 01 - Resource Limits ✅
- CPU requests: 500m, limits: 2000m
- Memory requests: 2Gi, limits: 3Gi
- Appropriate for ML workload requirements

### Rule 02 - Pod Security Baseline ✅
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance ✅
- Pinned image tag with SHA digest
- Uses trusted registry: `registry.bank.internal`
- No `:latest` tags

### Rule 04 - Naming & Label Conventions ✅
- Release name prefix: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### Rule 05 - Logging & Observability ✅
- Prometheus annotations for scraping
- JSON stdout logging (Spring Boot default)
- Metrics endpoint on port 8080

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness`
- Readiness probe: `/actuator/health/readiness`
- Appropriate timeouts and thresholds

## Deployment

```bash
kubectl apply -f k8s/
```

## Files

- `namespace.yaml` - Dedicated namespace with proper labels
- `deployment.yaml` - Main application deployment with security context
- `service.yaml` - ClusterIP service with Prometheus annotations
- `serviceaccount.yaml` - Dedicated service account
- `configmap.yaml` - ML model configuration
- `poddisruptionbudget.yaml` - High availability protection
- `networkpolicy.yaml` - Network security policies
