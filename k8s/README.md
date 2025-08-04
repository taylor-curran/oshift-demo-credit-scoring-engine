# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine that comply with the k8s-standards-library Rules 02-06.

## Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
- **CPU requests**: 500m (0.5 vCPU)
- **Memory requests**: 1536Mi (1.5 GB)
- **CPU limits**: 2000m (2 vCPU)
- **Memory limits**: 3072Mi (3 GB)
- Requests set to ~60% of limits for HPA headroom

### Rule 02 - Pod Security Baseline ✅
- `securityContext.runAsNonRoot: true`
- `securityContext.seccompProfile.type: RuntimeDefault`
- `securityContext.readOnlyRootFilesystem: true`
- `securityContext.capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance ✅
- **Development**: Uses pinned tag `registry.bank.internal/credit-scoring-engine:3.1.0`
- **Production**: Uses SHA digest for immutability
- Registry allow-list: `registry.bank.internal/*`
- Production images must have valid Cosign signatures (enforced by OpenShift Image Policies)

### Rule 04 - Naming & Label Conventions ✅
- **Release name prefix**: `credit-scoring-engine-{env}`
- **Mandatory labels**:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: dev|prod`
  - `managed-by: kubectl|helm`

### Rule 05 - Logging & Observability ✅
- **Structured JSON logging** to stdout (configured in application.properties)
- **Prometheus annotations**:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
  - `prometheus.io/path: "/actuator/prometheus"`
- Metrics exposed on `/actuator/prometheus` endpoint

### Rule 06 - Health Probes ✅
- **Liveness probe**: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- **Readiness probe**: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)
- Uses Spring Boot Actuator endpoints for JVM health monitoring

## File Structure

```
k8s/
├── deployment.yaml          # Development deployment
├── deployment-prod.yaml     # Production deployment (with SHA digest)
├── service.yaml            # Development service
├── service-prod.yaml       # Production service
├── configmap.yaml          # Development application configuration
├── configmap-prod.yaml     # Production application configuration
└── README.md              # This file
```

## Deployment Instructions

### Development Environment
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/configmap.yaml
```

### Production Environment
```bash
# Create secrets first (not included in this repo for security)
kubectl create secret generic credit-scoring-engine-secrets-prod \
  --from-literal=EXPERIAN_API_URL="https://api.experian.com/credit" \
  --from-literal=EQUIFAX_API_URL="https://api.equifax.com/ews" \
  --from-literal=TRANSUNION_API_URL="https://api.transunion.com/credit"

# Apply manifests
kubectl apply -f k8s/deployment-prod.yaml
kubectl apply -f k8s/service-prod.yaml
kubectl apply -f k8s/configmap-prod.yaml
```

## Migration from Cloud Foundry

This Kubernetes deployment maintains feature parity with the existing Cloud Foundry deployment (`manifest.yml`) while adding security and observability improvements:

- **Same resource allocation**: 4 instances, 3GB memory per instance
- **Same environment variables**: All CF env vars preserved
- **Enhanced security**: Non-root execution, read-only filesystem, dropped capabilities
- **Better observability**: Prometheus metrics, structured logging, health probes
- **Immutable deployments**: SHA-pinned images for production

## Monitoring & Observability

- **Metrics**: Automatically scraped by Prometheus via annotations
- **Logs**: JSON-formatted logs shipped to OpenShift Loki stack via fluent-bit sidecar
- **Health**: Liveness and readiness probes ensure service availability
- **Grafana**: Service will auto-appear in dashboards after Prometheus annotation injection
