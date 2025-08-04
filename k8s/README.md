# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with k8s-standards Rules 01-04.

## Standards Compliance

### Rule 01 - Resource Requests & Limits
- ✅ CPU requests: 600m (≥ 50m baseline)
- ✅ Memory requests: 1843Mi (≥ 128Mi baseline, 60% of 3072Mi limit)
- ✅ CPU limits: 1000m (≤ 4 vCPU baseline)
- ✅ Memory limits: 3072Mi (matches Cloud Foundry configuration)
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
- ✅ JSON stdout logging via application.properties
- ✅ Prometheus scraping annotations

### Rule 06 - Health Probes
- ✅ Liveness probe: `/actuator/health/liveness`
- ✅ Readiness probe: `/actuator/health/readiness`

## Deployment

```bash
kubectl apply -k k8s/
```

## Resource Allocation

- **Main container**: 600m/1000m CPU, 1843Mi/3072Mi memory (60% request-to-limit ratio)
- **Total memory**: 3072Mi (matches Cloud Foundry 3072M configuration)

## External Access

The service is exposed via Ingress on:
- `credit-scoring.internal.banking.com`
- `credit-api-v3.banking.com`

## Critical Notes

⚠️ **Before Production Deployment**:
1. Verify the image exists at `registry.bank.internal/credit-scoring-engine:3.1.0` with the specified SHA digest
2. Update the SHA digest if a newer version is available in your registry
3. Test the deployment in a dev/test environment first
