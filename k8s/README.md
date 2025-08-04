# Kubernetes Manifests - Credit Scoring Engine

This directory contains Kubernetes manifests for the Credit Scoring Engine application that comply with the organization's k8s standards.

## Compliance Summary

These manifests have been audited and updated to meet all required k8s standards:

### ✅ Rule 01 - Resource Requests & Limits
- **CPU requests**: 500m (0.5 vCPU)
- **CPU limits**: 2000m (2 vCPU) 
- **Memory requests**: 1536Mi (~1.5 GB)
- **Memory limits**: 3072Mi (3 GB)
- **Ratio**: Requests are ~60% of limits for HPA headroom

### ✅ Rule 02 - Pod Security Baseline
- **runAsNonRoot**: `true` - Container runs as non-root user
- **seccompProfile.type**: `RuntimeDefault` - Secure computing profile
- **readOnlyRootFilesystem**: `true` - Immutable root filesystem
- **capabilities.drop**: `["ALL"]` - All dangerous capabilities dropped
- **Volume mounts**: Writable volumes for `/tmp` and `/models` only

### ✅ Rule 03 - Image Provenance
- **No :latest tags**: Image uses pinned version `3.1.0`
- **Registry compliance**: Uses `registry.bank.internal/*` approved registry
- **Digest pinning**: Includes SHA256 digest for immutability
- **Signature verification**: Ready for Cosign/Sigstore validation

### ✅ Rule 04 - Naming & Label Conventions
- **Release name**: `pe-eng-credit-scoring-engine-prod` format
- **app.kubernetes.io/name**: `credit-scoring-engine`
- **app.kubernetes.io/version**: `3.1.0`
- **app.kubernetes.io/part-of**: `retail-banking`
- **environment**: `prod`
- **managed-by**: `openshift`

### ✅ Rule 05 - Logging & Observability
- **Prometheus annotations**: `prometheus.io/scrape: "true"` and `prometheus.io/port: "8080"`
- **Metrics endpoint**: `/metrics` exposed on port 8080
- **Structured logging**: Application configured for JSON output to stdout

### ✅ Rule 06 - Health Probes
- **Liveness probe**: `/actuator/health/liveness` with 30s initial delay, 3 failure threshold
- **Readiness probe**: `/actuator/health/readiness` with 10s initial delay, 1 failure threshold
- **Spring Boot Actuator**: Configured for health check endpoints

## Files Overview

- **namespace.yaml**: Dedicated namespace with proper labeling
- **deployment.yaml**: Main application deployment with 4 replicas
- **service.yaml**: ClusterIP service with Prometheus annotations
- **configmap.yaml**: Application configuration and properties
- **secret.yaml**: Template for sensitive configuration (passwords, API keys)
- **ingress.yaml**: External access routing for internal and API domains

## Migration from Cloud Foundry

This replaces the original `manifest.yml` Cloud Foundry configuration with equivalent Kubernetes resources:

| Cloud Foundry | Kubernetes | Notes |
|---------------|------------|-------|
| `instances: 4` | `replicas: 4` | Same scaling |
| `memory: 3072M` | `limits.memory: 3072Mi` | Same memory allocation |
| `env:` section | `env:` + ConfigMap | Environment variables preserved |
| `services:` | External services | Managed separately in k8s |
| `routes:` | Ingress | HTTP routing configuration |
| `health-check-*` | Health probes | Actuator endpoints |

## Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/

# Verify deployment
kubectl get pods -n credit-scoring
kubectl describe deployment pe-eng-credit-scoring-engine-prod -n credit-scoring

# Check compliance
kubectl get pod <pod-name> -n credit-scoring -o yaml | grep -A 10 securityContext
```

## Security Notes

- All containers run as non-root with read-only root filesystem
- Sensitive data should be managed through external secret management systems
- Network policies should be applied for additional isolation
- Image signatures should be verified in production environments
