# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s standards library requirements.

## Standards Compliance

### Rule 02 - Security Context
- ✅ `runAsNonRoot: true` - Containers run as non-root user (UID 1001)
- ✅ `seccompProfile.type: RuntimeDefault` - Runtime default seccomp profile applied
- ✅ `readOnlyRootFilesystem: true` - Root filesystem is read-only
- ✅ `capabilities.drop: ["ALL"]` - All Linux capabilities dropped

### Rule 04 - Naming & Labels
- ✅ `app.kubernetes.io/name: credit-scoring-engine` - Stable app identifier
- ✅ `app.kubernetes.io/version: "3.1.0"` - Traceable release version
- ✅ `app.kubernetes.io/part-of: retail-banking` - Business grouping
- ✅ `environment: prod` - Environment designation
- ✅ `managed-by: helm` - Tool provenance
- ✅ Release name prefix: `pe-eng-credit-scoring-engine-prod`

### Rule 05 - Logging & Observability
- ✅ `prometheus.io/scrape: "true"` - Enable Prometheus scraping
- ✅ `prometheus.io/port: "8080"` - Metrics port specification
- ✅ `prometheus.io/path: "/actuator/prometheus"` - Metrics endpoint path

### Rule 06 - Health Probes
- ✅ Liveness probe: `/actuator/health/liveness`
- ✅ Readiness probe: `/actuator/health/readiness`
- ✅ Proper timing configuration for JVM applications

## Deployment Options

### Option 1: Direct Kubernetes Manifests
```bash
kubectl apply -f k8s/
```

### Option 2: Helm Chart (Recommended)
```bash
helm install pe-eng-credit-scoring-engine-prod ./charts/credit-scoring-engine \
  --namespace credit-scoring \
  --create-namespace
```

## Image Requirements

The deployment uses images from the approved registry:
- `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`

Images must be:
- Tagged with specific versions (no `:latest`)
- Signed with Cosign for production use
- From approved registries only

## Resource Allocation

- **CPU**: 500m requests, 2000m limits
- **Memory**: 1536Mi requests, 3072Mi limits
- **Replicas**: 4 instances for high availability

## Security Features

- Non-root user execution (UID/GID 1001)
- Read-only root filesystem with writable `/tmp` volume
- All Linux capabilities dropped
- Runtime default seccomp profile
- No privilege escalation allowed
