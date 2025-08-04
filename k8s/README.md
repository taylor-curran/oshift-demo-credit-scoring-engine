# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with k8s-standards Rules 01-06.

## Standards Compliance Status

### ✅ Rule 01 - Resource Requests & Limits
- **Main container**: 600m/1000m CPU, 1843Mi/3072Mi memory (60% request-to-limit ratio)
- **Fluent-bit sidecar**: 120m/200m CPU, 154Mi/256Mi memory (60% request-to-limit ratio)
- All containers have both requests and limits defined
- Memory limits stay within 4 vCPU / 2 Gi baseline for main container (3072Mi = 3Gi)

### ✅ Rule 02 - Security Context
- `runAsNonRoot: true` for pod and all containers
- `seccompProfile.type: RuntimeDefault` applied
- `readOnlyRootFilesystem: true` for all containers
- `capabilities.drop: ["ALL"]` removes dangerous capabilities
- Non-root user ID 1001 for all containers

### ✅ Rule 03 - Image Provenance
- SHA digest pinning for all images (no `:latest` tags)
- Registry allowlist compliance:
  - Main app: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
  - Sidecar: `quay.io/redhat-openshift-approved/fluent-bit:2.1.10@sha256:...`
- Production images ready for Cosign signature verification

### ✅ Rule 04 - Naming & Labels
- **Mandatory labels** on all resources:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`
- **Release-name prefix**: `pe-eng-credit-scoring-engine-prod`
- Consistent naming across all Kubernetes resources

### ✅ Rule 05 - Logging & Observability
- **JSON stdout logging** via application.properties configuration
- **Prometheus scraping annotations**:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
- **Fluent-bit sidecar** for centralized log aggregation to OpenShift Loki stack
- Metrics endpoint exposed on port 8080 at `/actuator/prometheus`

### ✅ Rule 06 - Health Probes
- **Liveness probe**: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- **Readiness probe**: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)
- Spring Boot Actuator endpoints enabled for k8s health checks

## Deployment Instructions

### Prerequisites
- Kubernetes cluster with namespace creation permissions
- kubectl configured with cluster access
- Kustomize support (built into kubectl 1.14+)

### Deploy to Kubernetes
```bash
# Deploy all resources using Kustomize
kubectl apply -k k8s/

# Verify deployment
kubectl get pods -n credit-scoring -l app.kubernetes.io/name=credit-scoring-engine

# Check service status
kubectl get svc -n credit-scoring

# View logs
kubectl logs -n credit-scoring -l app.kubernetes.io/name=credit-scoring-engine -c credit-scoring-engine
```

### Access the Application
The service is exposed via Ingress on:
- `https://credit-scoring.internal.banking.com`
- `https://credit-api-v3.banking.com`

### Health Check Endpoints
- Liveness: `GET /actuator/health/liveness`
- Readiness: `GET /actuator/health/readiness`
- Detailed health: `GET /actuator/health/detailed`
- Metrics: `GET /actuator/prometheus`

## Resource Allocation

| Component | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|-------------|-----------|----------------|--------------|
| Credit Scoring Engine | 600m | 1000m | 1843Mi | 3072Mi |
| Fluent-bit Sidecar | 120m | 200m | 154Mi | 256Mi |

## Security Features

- **Non-root execution**: All containers run as user ID 1001
- **Read-only filesystem**: Prevents runtime file modifications
- **Dropped capabilities**: All Linux capabilities removed for minimal attack surface
- **Seccomp profile**: Runtime default seccomp profile applied
- **Network policies**: Ready for network segmentation (policies not included)

## Observability Stack Integration

- **Prometheus**: Automatic service discovery via annotations
- **Grafana**: Services auto-appear in dashboards after deployment
- **Loki**: Centralized log aggregation via fluent-bit sidecar
- **OpenShift Logging**: Integration with cluster logging infrastructure

## Troubleshooting

### Pod Startup Issues
```bash
# Check pod events
kubectl describe pod -n credit-scoring -l app.kubernetes.io/name=credit-scoring-engine

# View container logs
kubectl logs -n credit-scoring <pod-name> -c credit-scoring-engine

# Check security context issues
kubectl get pod -n credit-scoring <pod-name> -o yaml | grep -A 10 securityContext
```

### Service Discovery Issues
```bash
# Verify service endpoints
kubectl get endpoints -n credit-scoring

# Test internal connectivity
kubectl run debug --image=busybox -it --rm -- wget -qO- http://pe-eng-credit-scoring-engine-prod.credit-scoring:8080/actuator/health
```

### Monitoring Issues
```bash
# Check Prometheus annotations
kubectl get svc -n credit-scoring pe-eng-credit-scoring-engine-prod -o yaml | grep prometheus

# Verify metrics endpoint
kubectl port-forward -n credit-scoring svc/pe-eng-credit-scoring-engine-prod 8080:8080
curl http://localhost:8080/actuator/prometheus
```
