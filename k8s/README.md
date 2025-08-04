# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine application in compliance with organizational k8s standards.

## Standards Compliance

### Rule 02 - Security Context Baseline
- ✅ `runAsNonRoot: true` - All containers run as non-root user (1001)
- ✅ `seccompProfile.type: RuntimeDefault` - Seccomp profile applied
- ✅ `readOnlyRootFilesystem: true` - Root filesystem is read-only
- ✅ `capabilities.drop: ["ALL"]` - All capabilities dropped

### Rule 03 - Image Provenance
- ✅ No `:latest` tags - Uses pinned version `3.1.0` with SHA digest
- ✅ Registry allow-list - Uses `registry.bank.internal/*` approved registry
- ✅ Signed images - Production images must have valid Cosign signatures

### Rule 04 - Naming & Label Conventions
- ✅ Release name prefix: `pe-eng-credit-scoring-engine-prod`
- ✅ Mandatory labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### Rule 05 - Logging & Observability
- ✅ Prometheus annotations for metrics scraping
- ✅ Health probes configured for Spring Boot Actuator endpoints
- ✅ Structured logging via JSON stdout (application level)

### Rule 06 - Health Probes
- ✅ Liveness probe: `/actuator/health/liveness`
- ✅ Readiness probe: `/actuator/health/readiness`
- ✅ Appropriate timeouts and failure thresholds

## Deployment

```bash
# Apply all manifests
kubectl apply -k k8s/

# Or apply individually
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/networkpolicy.yaml
```

## Resource Requirements

- **CPU**: 1000m requests, 2000m limits per pod
- **Memory**: 2Gi requests, 3Gi limits per pod
- **Replicas**: 4 instances for high availability
- **Storage**: Read-only root filesystem with temporary volumes

## Security Features

- Non-root user execution (UID 1001)
- Read-only root filesystem
- Network policies restricting ingress/egress
- Secrets management for sensitive data
- Capability dropping for enhanced security
