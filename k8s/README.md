# Kubernetes Manifests - Standards Compliant

This directory contains Kubernetes manifests for the Credit Scoring Engine that are fully compliant with enterprise k8s standards.

## Standards Compliance

### ✅ Rule 01 - Resource Limits
- **CPU requests**: 1200m (60% of 2000m limit)
- **Memory requests**: 1800Mi (60% of 3Gi limit)
- **CPU limits**: 2000m
- **Memory limits**: 3Gi (matching Cloud Foundry 3072M allocation)

### ✅ Rule 02 - Pod Security Baseline
- **runAsNonRoot**: true
- **runAsUser/runAsGroup**: 1001 (non-root user)
- **fsGroup**: 1001
- **seccompProfile**: RuntimeDefault
- **readOnlyRootFilesystem**: true
- **allowPrivilegeEscalation**: false
- **capabilities**: drop ["ALL"]

### ✅ Rule 03 - Image Provenance
- **Registry**: registry.bank.internal/* (trusted internal registry)
- **Tag**: 3.1.0 (no :latest tags)
- **Digest**: SHA256 hash included for immutable image reference

### ✅ Rule 04 - Naming & Label Conventions
- **Release name**: pe-eng-credit-scoring-engine-prod
- **Mandatory labels**:
  - `app.kubernetes.io/name`: credit-scoring-engine
  - `app.kubernetes.io/version`: "3.1.0"
  - `app.kubernetes.io/part-of`: retail-banking
  - `environment`: prod
  - `managed-by`: helm

### ✅ Rule 05 - Logging & Observability
- **Prometheus annotations**: prometheus.io/scrape, prometheus.io/port, prometheus.io/path
- **Metrics port**: 8080 (Spring Boot Actuator)
- **JSON logging**: Configured via Spring Boot profiles

### ✅ Rule 06 - Health Probes
- **Liveness probe**: /actuator/health/liveness (60s initial delay, 30s period)
- **Readiness probe**: /actuator/health/readiness (30s initial delay, 10s period)
- **Spring Boot Actuator**: Health endpoints for JVM applications

## Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/

# Or apply individually
kubectl apply -f k8s/serviceaccount.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## Security Features

- **ServiceAccount**: Dedicated service account for RBAC compliance
- **Volume Mounts**: 
  - `/tmp` as emptyDir for temporary files (readOnlyRootFilesystem compatibility)
  - `/models` as configMap mount for ML model configuration
- **Health Probes**: Liveness and readiness probes using Spring Boot Actuator endpoints
- **Prometheus Integration**: Annotations for metrics scraping

## Configuration

Environment variables are configured directly in the deployment manifest, matching the Cloud Foundry configuration from `manifest.yml`.

Key configuration includes:
- Credit bureau API endpoints
- ML model versions and paths
- Compliance settings (FCRA, ECOA)
- JVM optimization settings
