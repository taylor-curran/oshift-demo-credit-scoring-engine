# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the banking platform's k8s standards.

## Standards Compliance

### ✅ Rule 01 - Resource Requests & Limits
- CPU requests: 500m, limits: 2000m
- Memory requests: 1536Mi, limits: 3072Mi
- Follows 60% request-to-limit ratio for HPA headroom

### ✅ Rule 02 - Pod Security Baseline
- `runAsNonRoot: true` with user/group 1001
- `readOnlyRootFilesystem: true` with writable /tmp volume
- `capabilities.drop: ["ALL"]` - all dangerous capabilities dropped
- `seccompProfile.type: RuntimeDefault` - secure computing profile

### ✅ Rule 03 - Immutable, Trusted Images
- Uses pinned image with SHA digest: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:abc123def456789`
- No `:latest` tags used
- Images from approved internal registry

### ✅ Rule 04 - Naming & Label Conventions
- Release name: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### ✅ Rule 05 - Logging & Observability
- Prometheus scraping annotations on pods and service
- Metrics endpoint: `/metrics` on port 8080
- JSON logging to stdout (configured via Spring Boot)

### ✅ Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failures)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure)

## Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n credit-scoring

# View logs
kubectl logs -f deployment/pe-eng-credit-scoring-engine-prod -n credit-scoring
```

## Configuration

The deployment maintains all environment variables from the original Cloud Foundry manifest.yml:
- Credit bureau API configurations
- ML model settings
- Compliance and regulatory flags
- Database and service connections

## Security Features

- Non-root execution (UID/GID 1001)
- Read-only root filesystem with writable /tmp
- Dropped all Linux capabilities
- Secure computing profile enabled
- TLS-enabled ingress with proper certificates
