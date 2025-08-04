# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s standards library (Rules 02-06).

## Standards Compliance

### Rule 02 - Security Context Baseline
- ✅ `runAsNonRoot: true`
- ✅ `seccompProfile.type: RuntimeDefault`
- ✅ `readOnlyRootFilesystem: true`
- ✅ `capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance
- ✅ No `:latest` tags used
- ✅ Pinned to specific version with SHA digest
- ✅ Uses trusted registry: `registry.bank.internal`

### Rule 04 - Naming & Labels
- ✅ Mandatory labels present:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`
- ✅ Release name prefix: `pe-eng-credit-scoring-engine-prod`

### Rule 05 - Logging & Observability
- ✅ Prometheus annotations:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
  - `prometheus.io/path: "/actuator/prometheus"`

### Rule 06 - Health Probes
- ✅ Liveness probe: `/actuator/health/liveness`
- ✅ Readiness probe: `/actuator/health/readiness`

## Files

- `namespace.yaml` - Namespace definition with proper labels
- `deployment.yaml` - Main application deployment with security context and health probes
- `service.yaml` - Service definition with Prometheus annotations
- `configmap.yaml` - Configuration for ML models
- `ingress.yaml` - Ingress configuration for external access
- `networkpolicy.yaml` - Network security policies

## Deployment

```bash
kubectl apply -f k8s/
```

## Notes

- The image reference includes a placeholder SHA digest that should be updated with the actual digest
- ML model data in ConfigMap is a placeholder and should be replaced with actual model files
- Network policies are configured for typical banking environment requirements
