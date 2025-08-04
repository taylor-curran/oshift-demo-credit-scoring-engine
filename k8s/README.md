# Kubernetes Manifests - Standards Compliance

This directory contains Kubernetes manifests for the Credit Scoring Engine that comply with all organizational k8s standards (Rules 01-06).

## Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
- **CPU requests**: 500m (main container), 50m (fluent-bit sidecar)
- **Memory requests**: 1536Mi (main container), 64Mi (fluent-bit sidecar)  
- **CPU limits**: 2000m (main container), 100m (fluent-bit sidecar)
- **Memory limits**: 3072Mi (main container), 128Mi (fluent-bit sidecar)
- **Requests ≈ 60% of limits** for HPA headroom

### Rule 02 - Pod Security Baseline ✅
- `securityContext.runAsNonRoot: true`
- `securityContext.seccompProfile.type: RuntimeDefault`
- `securityContext.readOnlyRootFilesystem: true`
- `securityContext.capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance ✅
- **Tag pinning**: Uses specific version tags with SHA256 digests
- **Registry allow-list**: All images from `registry.bank.internal/*`
- **Cosign signatures**: Production images verified by OpenShift Image Policies

### Rule 04 - Naming & Labels ✅
- **Release name prefix**: `pe-eng-credit-scoring-engine-prod`
- **Mandatory labels**:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### Rule 05 - Logging & Observability ✅
- **JSON logs**: Structured logging to stdout
- **Fluent-bit sidecar**: Ships logs to OpenShift Loki stack
- **Prometheus metrics**: Exposed on port 8080 at `/metrics`
- **Required annotations**:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`

### Rule 06 - Health Probes ✅
- **Liveness probe**: `/actuator/health/liveness`, 30s initial delay, 3 failure threshold
- **Readiness probe**: `/actuator/health/readiness`, 10s initial delay, 1 failure threshold

## Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/

# Verify deployment
kubectl get pods -l app.kubernetes.io/name=credit-scoring-engine
kubectl describe deployment pe-eng-credit-scoring-engine-prod
```

## Files

- `deployment.yaml` - Main application deployment with sidecar
- `service.yaml` - ClusterIP service for internal access
- `configmap.yaml` - Application configuration
- `fluent-bit-sidecar.yaml` - Log shipping configuration

## Migration from Cloud Foundry

This replaces the previous `manifest.yml` Cloud Foundry configuration with compliant Kubernetes manifests that maintain the same functionality while meeting all organizational security and operational standards.
