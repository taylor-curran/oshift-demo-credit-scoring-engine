# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with k8s-standards Rules 01-06.

## Standards Compliance

### Rule 01 - Resource Limits
- ✅ CPU/memory requests and limits properly configured
- ✅ Main container: 600m/1000m CPU, 1843Mi/3072Mi memory (60% request-to-limit ratio)
- ✅ Fluent-bit sidecar: 120m/200m CPU, 154Mi/256Mi memory (60% request-to-limit ratio)

### Rule 02 - Security Context
- ✅ `runAsNonRoot: true`
- ✅ `seccompProfile.type: RuntimeDefault`
- ✅ `readOnlyRootFilesystem: true`
- ✅ `capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance
- ✅ SHA digest pinning for all images
- ✅ Registry allowlist compliance (`registry.bank.internal/*`, `quay.io/redhat-openshift-approved/*`)
- ✅ No `:latest` tags

### Rule 04 - Naming & Labels
- ✅ Mandatory labels: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/part-of`, `environment`, `managed-by`
- ✅ Release-name prefix: `pe-eng-credit-scoring-engine-prod`

### Rule 05 - Logging & Observability
- ✅ JSON stdout logging via application.properties
- ✅ Prometheus scraping annotations
- ✅ Fluent-bit sidecar for log aggregation

### Rule 06 - Health Probes
- ✅ Liveness probe: `/actuator/health/liveness`
- ✅ Readiness probe: `/actuator/health/readiness`

## Deployment

```bash
kubectl apply -k k8s/
```

## Resource Allocation

- **Main container**: 600m/1000m CPU, 1843Mi/3072Mi memory (60% request-to-limit ratio)
- **Fluent-bit sidecar**: 120m/200m CPU, 154Mi/256Mi memory (60% request-to-limit ratio)

## External Access

The service is exposed via Ingress on:
- `credit-scoring.internal.banking.com`
- `credit-api-v3.banking.com`

## Testing

Run unit tests to verify application functionality:
```bash
mvn test
```

## Notes

- SHA digests in image references should be verified against your actual registry before production deployment
- Fluent-bit is configured to collect logs from `/var/log/containers/*.log` and forward to Loki
- All containers run as non-root user (1001) with read-only root filesystem
- Prometheus metrics are exposed on port 8080 with automatic scraping enabled
