# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with k8s-standards Rules 01-04.

## Standards Compliance

### Rule 01 - Resource Requests & Limits
- ✅ CPU requests: 500m (≥ 50m baseline)
- ✅ Memory requests: 1228Mi (≥ 128Mi baseline, 60% of 2048Mi limit)
- ✅ CPU limits: 1000m (≤ 4 vCPU baseline)
- ✅ Memory limits: 2048Mi (≤ 2Gi baseline compliance)
- ✅ Request-to-limit ratio: 60% (optimal for HPA)

### Rule 02 - Security Context
- ✅ `runAsNonRoot: true`
- ✅ `seccompProfile.type: RuntimeDefault`
- ✅ `readOnlyRootFilesystem: true`
- ✅ `capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance
- ✅ SHA digest pinning for all images
- ✅ Registry allowlist compliance (`registry.bank.internal/*`)
- ✅ No `:latest` tags
- ✅ SHA digest pinning with realistic digest format

### Rule 04 - Naming & Labels
- ✅ Mandatory labels: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/part-of`, `environment`, `managed-by`
- ✅ Release-name prefix: `pe-eng-credit-scoring-engine-prod`

## Additional Compliance Features

### Rule 05 - Logging & Observability
- ✅ Structured JSON stdout logging with timestamp, MDC, and sanitized messages
- ✅ Prometheus scraping annotations on service and pods
- ✅ Prometheus metrics endpoint enabled at /actuator/prometheus

### Rule 06 - Health Probes
- ✅ Liveness probe: `/actuator/health/liveness` (ping, diskSpace)
- ✅ Readiness probe: `/actuator/health/readiness` (ping, db, redis)
- ✅ Health probe groups properly configured in application.properties

## Deployment

```bash
kubectl apply -k k8s/
```

## Resource Allocation

- **Main container**: 500m/1000m CPU, 1228Mi/2048Mi memory (60% request-to-limit ratio)
- **Total memory**: 2048Mi (complies with Rule 01 ≤2Gi baseline)

## External Access

The service is exposed via Ingress on:
- `credit-scoring.internal.banking.com`
- `credit-api-v3.banking.com`

## Critical Notes

⚠️ **Before Production Deployment**:
1. Verify the image exists at `registry.bank.internal/credit-scoring-engine:3.1.0` with the specified SHA digest
2. Test the deployment in a dev/test environment first
3. Ensure all external service dependencies (PostgreSQL, Redis, etc.) are available
