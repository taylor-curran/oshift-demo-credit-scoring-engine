# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes deployment manifests that comply with the k8s-standards-library requirements.

## Standards Compliance

### Rule 02 - Security Context
- ✅ `runAsNonRoot: true` - All containers run as non-root user (UID 1001)
- ✅ `seccompProfile.type: RuntimeDefault` - Runtime default seccomp profile applied
- ✅ `readOnlyRootFilesystem: true` - Root filesystem is read-only
- ✅ `capabilities.drop: ["ALL"]` - All Linux capabilities dropped

### Rule 03 - Image Provenance
- ✅ No `:latest` tags - Image uses pinned version with SHA digest
- ✅ Registry allow-list - Uses approved `registry.bank.internal` registry
- ✅ Cosign signatures - Production images verified by OpenShift Image Policies

### Rule 04 - Naming & Labels
- ✅ Mandatory labels applied to all resources:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`
- ✅ Release-name prefix: `pe-eng-credit-scoring-engine-prod`

### Rule 05 - Observability
- ✅ Prometheus annotations for metrics scraping
- ✅ Health probes configured for liveness and readiness
- ✅ Structured logging via Spring Boot Actuator

## Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/

# Verify deployment
kubectl get pods -n credit-scoring
kubectl get svc -n credit-scoring
```

## Resources

- **CPU**: 500m requests, 2000m limits
- **Memory**: 2Gi requests, 3Gi limits
- **Replicas**: 4 instances for high availability
- **Health Checks**: Spring Boot Actuator endpoints
