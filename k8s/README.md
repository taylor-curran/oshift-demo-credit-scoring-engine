# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with enterprise k8s standards for the Credit Scoring Engine application.

## Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
- **CPU Requests**: 500m (0.5 vCPU)
- **CPU Limits**: 2000m (2 vCPU) 
- **Memory Requests**: 1536Mi (~1.5GB)
- **Memory Limits**: 3072Mi (3GB)
- **Ratio**: Requests are ~75% of limits for HPA headroom

### Rule 02 - Pod Security Baseline ✅
- **runAsNonRoot**: `true` (runs as user 1001)
- **seccompProfile**: `RuntimeDefault`
- **readOnlyRootFilesystem**: `true`
- **capabilities**: Drop `["ALL"]`
- **allowPrivilegeEscalation**: `false`

### Rule 03 - Image Provenance ✅
- **Registry**: `registry.bank.internal` (trusted internal registry)
- **Tag**: Pinned to `3.1.0` (no `:latest`)
- **Digest**: SHA256 digest for immutable reference
- **Signature**: Ready for Cosign verification

### Rule 04 - Naming & Label Conventions ✅
- **Release Name**: `pe-eng-credit-scoring-engine-prod`
- **Standard Labels**:
  - `app.kubernetes.io/name`: `credit-scoring-engine`
  - `app.kubernetes.io/version`: `3.1.0`
  - `app.kubernetes.io/part-of`: `retail-banking`
  - `environment`: `prod`
  - `managed-by`: `helm`

### Rule 05 - Logging & Observability ✅
- **Prometheus Scraping**: `prometheus.io/scrape: "true"`
- **Metrics Port**: `prometheus.io/port: "8080"`
- **JSON Logging**: Application configured for structured stdout logging
- **Auto-discovery**: Service automatically appears in Grafana dashboards

### Rule 06 - Health Probes ✅
- **Liveness Probe**: `/actuator/health/detailed` endpoint
- **Readiness Probe**: `/actuator/health/detailed` endpoint
- **Spring Boot Actuator**: JVM application health monitoring

## Files

- `namespace.yaml` - Dedicated namespace with proper labels
- `deployment.yaml` - Main application deployment with security contexts
- `service.yaml` - ClusterIP service for internal communication
- `configmap.yaml` - ML model configuration data
- `Chart.yaml` - Helm chart metadata
- `values.yaml` - Configurable values for different environments

## Deployment

```bash
# Apply manifests directly
kubectl apply -f k8s/

# Or use Helm
helm install credit-scoring-engine k8s/ --namespace credit-scoring --create-namespace
```

## Migration from Cloud Foundry

This replaces the Cloud Foundry `manifest.yml` with Kubernetes-native deployment patterns while maintaining the same application configuration and scaling characteristics.
