# Kubernetes Manifests - Credit Scoring Engine

This directory contains Kubernetes manifests for the Credit Scoring Engine that comply with all 6 banking k8s standards.

## Standards Compliance

### ✅ Rule 01 - Resource Requests & Limits
- **CPU**: requests: 600m, limits: 1000m (60% ratio for HPA headroom)
- **Memory**: requests: 1228Mi, limits: 2048Mi (60% ratio, reduced from 3072Mi to meet ≤2Gi limit)
- **JVM Heap**: Adjusted from 2560m to 1536m to accommodate memory limit reduction

### ✅ Rule 02 - Pod Security Baseline
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### ✅ Rule 03 - Image Provenance
- Pinned image tags with SHA256 digests
- Uses approved registries: `registry.bank.internal/*` and `quay.io/redhat-openshift-approved/*`
- No `:latest` tags

### ✅ Rule 04 - Naming & Label Conventions
- Release name prefix: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/part-of`, `environment`, `managed-by`

### ✅ Rule 05 - Logging & Observability
- JSON structured logging via fluent-bit sidecar
- Prometheus scraping annotations: `prometheus.io/scrape: "true"`, `prometheus.io/port: "8080"`
- Fluent-bit ships logs to OpenShift Loki stack

### ✅ Rule 06 - Health Probes
- **Liveness**: `/actuator/health/liveness`, 30s initial delay, 3 failure threshold
- **Readiness**: `/actuator/health/readiness`, 10s initial delay, 1 failure threshold

## Deployment

Deploy all resources using kustomize:

```bash
kubectl apply -k k8s/
```

Or deploy individual resources:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/fluent-bit-configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

## Resources Created

- **Namespace**: `credit-scoring`
- **Deployment**: `pe-eng-credit-scoring-engine-prod` (4 replicas)
- **Service**: `pe-eng-credit-scoring-engine-prod` (ClusterIP)
- **Ingress**: `pe-eng-credit-scoring-engine-prod` (2 hosts)
- **ConfigMaps**: `credit-scoring-config`, `fluent-bit-config`

## Key Changes from Cloud Foundry

- **Memory Reduction**: 3072Mi → 2048Mi (33% reduction to meet Rule 01 ≤2Gi limit)
- **JVM Heap Adjustment**: 2560m → 1536m (to accommodate memory limit)
- **Security Hardening**: Non-root user, read-only filesystem, dropped capabilities
- **Observability**: Added fluent-bit sidecar for JSON log shipping
- **Health Monitoring**: Spring Boot Actuator endpoints for liveness/readiness

## Monitoring & Health Checks

- **Application Port**: 8080
- **Health Endpoints**: 
  - Liveness: `http://localhost:8080/actuator/health/liveness`
  - Readiness: `http://localhost:8080/actuator/health/readiness`
  - Detailed: `http://localhost:8080/actuator/health/detailed`
- **Metrics**: `http://localhost:8080/metrics` (Prometheus format)
- **Fluent-bit Admin**: `http://localhost:2020` (sidecar)

## Important Notes

⚠️ **Memory Limit Reduction**: The memory allocation was reduced by 33% (3072Mi → 2048Mi) to comply with Rule 01. This change requires validation under production load to ensure the application doesn't experience OOM kills.

🔒 **Security Context**: The application now runs as non-root with a read-only root filesystem. Temporary files are written to mounted emptyDir volumes at `/tmp` and `/logs`.

📊 **Logging**: All application logs are now processed by the fluent-bit sidecar and shipped as structured JSON to the OpenShift Loki stack for centralized log aggregation.
