# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine with full compliance to k8s standards (Rules 01-06).

## Standards Compliance

### Rule 01 - Resource Limits
- **CPU Requests/Limits**: Configured per environment (dev: 250m/1000m, test: 375m/1500m, prod: 500m/2000m)
- **Memory Requests/Limits**: Configured per environment (dev: 768Mi/1536Mi, test: 1152Mi/2304Mi, prod: 1536Mi/3072Mi)
- **Requests ≈ 60% of limits** for HPA headroom

### Rule 02 - Pod Security Baseline
- `runAsNonRoot: true` - Runs as user 1001
- `seccompProfile.type: RuntimeDefault` - Uses runtime default seccomp profile
- `readOnlyRootFilesystem: true` - Filesystem is read-only
- `capabilities.drop: ["ALL"]` - All dangerous capabilities dropped
- `allowPrivilegeEscalation: false` - No privilege escalation

### Rule 03 - Image Provenance
- Uses pinned image tags from internal registry: `registry.bank.internal/credit-scoring-engine:3.1.0`
- Environment-specific tags (dev: 3.1.0-dev, test: 3.1.0-test, prod: 3.1.0)
- No `:latest` tags used

### Rule 04 - Naming & Label Conventions
- **Mandatory labels**: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/part-of`, `environment`, `managed-by`
- **Release-name prefix**: `pe-eng-credit-scoring-{env}-` format
- **Business grouping**: `retail-banking` part-of label

### Rule 05 - Logging & Observability
- **Prometheus annotations**: `prometheus.io/scrape: "true"`, `prometheus.io/port: "8080"`, `prometheus.io/path: "/actuator/prometheus"`
- **JSON logging**: Application configured for structured JSON output to stdout
- **Metrics endpoint**: Spring Boot Actuator exposes metrics at `/actuator/prometheus`

### Rule 06 - Health Probes
- **Liveness probe**: `/actuator/health/liveness` with 30s initial delay, 3 failure threshold
- **Readiness probe**: `/actuator/health/readiness` with 10s initial delay, 1 failure threshold
- **Spring Boot Actuator**: Leverages built-in health endpoints

## Directory Structure

```
k8s/
├── base/                           # Base Kubernetes manifests
│   ├── kustomization.yaml         # Base kustomization
│   ├── deployment.yaml            # Main deployment configuration
│   ├── service.yaml               # Service definition
│   └── configmap.yaml             # Application configuration
└── overlays/                      # Environment-specific overlays
    ├── dev/                       # Development environment
    │   ├── kustomization.yaml     # Dev-specific patches
    │   └── deployment-patch.yaml  # Dev resource adjustments
    ├── test/                      # Test environment
    │   ├── kustomization.yaml     # Test-specific patches
    │   └── deployment-patch.yaml  # Test resource adjustments
    └── prod/                      # Production environment
        ├── kustomization.yaml     # Prod-specific patches
        └── deployment-patch.yaml  # Prod resource adjustments
```

## Deployment

### Prerequisites
- Kustomize CLI installed
- Access to `registry.bank.internal` container registry
- Kubernetes cluster with appropriate namespaces created

### Deploy to Development
```bash
kubectl apply -k k8s/overlays/dev
```

### Deploy to Test
```bash
kubectl apply -k k8s/overlays/test
```

### Deploy to Production
```bash
kubectl apply -k k8s/overlays/prod
```

## Environment Differences

| Environment | Replicas | CPU Request/Limit | Memory Request/Limit | Image Tag | Profile |
|-------------|----------|-------------------|---------------------|-----------|---------|
| dev         | 2        | 250m/1000m       | 768Mi/1536Mi        | 3.1.0-dev | dev,scoring |
| test        | 3        | 375m/1500m       | 1152Mi/2304Mi       | 3.1.0-test | test,scoring |
| prod        | 4        | 500m/2000m       | 1536Mi/3072Mi       | 3.1.0     | production,scoring |

## Security Features

- **Non-root execution**: All containers run as user 1001
- **Read-only filesystem**: Root filesystem is immutable
- **Dropped capabilities**: All Linux capabilities removed for security
- **Seccomp profile**: Runtime default seccomp profile applied
- **Volume mounts**: Writable volumes only for /tmp, /app/cache, and /app/logs

## Monitoring & Observability

- **Prometheus metrics**: Automatically scraped via annotations
- **Health checks**: Kubernetes probes monitor application health
- **Structured logging**: JSON logs output to stdout for centralized collection
- **Spring Boot Actuator**: Comprehensive application monitoring endpoints
