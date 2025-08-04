# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s standards for the credit scoring engine application.

## Standards Compliance

These manifests comply with the following k8s standards:

### Rule 01 - Resource Requests & Limits
- CPU requests: 300m (0.3 vCPU)
- Memory requests: 1536Mi (1.5 GB)
- CPU limits: 2000m (2 vCPU)
- Memory limits: 3072Mi (3 GB)
- Requests are ~60% of limits for HPA headroom

### Rule 02 - Pod Security Baseline
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### Rule 03 - Immutable, Trusted Images
- Uses pinned image tag with SHA digest
- Image from trusted registry: `registry.bank.internal/*`
- No `:latest` tags

### Rule 04 - Naming & Label Conventions
- Release name: `pe-eng-credit-scoring-prod`
- Mandatory labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: openshift`

### Rule 05 - Logging & Observability
- Prometheus scraping annotations
- JSON structured logging to stdout
- Metrics endpoint at `/metrics`

### Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness` (30s initial delay)
- Readiness probe: `/actuator/health/readiness` (10s initial delay)

## Deployment

To deploy these manifests:

```bash
kubectl apply -k k8s/
```

## Migration from Cloud Foundry

These manifests replace the `manifest.yml` Cloud Foundry configuration with equivalent Kubernetes resources:

- **Applications** → Deployment with 4 replicas
- **Memory/Disk** → Resource requests/limits
- **Environment variables** → Container env vars
- **Services** → Kubernetes Services and ConfigMaps
- **Routes** → Ingress resources
- **Health checks** → Liveness/Readiness probes
