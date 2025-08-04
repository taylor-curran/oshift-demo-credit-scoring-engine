# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine application that comply with enterprise k8s standards.

## Standards Compliance

### ✅ Rule 01 - Resource Requests & Limits
- CPU requests: 1200m (1.2 vCPU)
- CPU limits: 2000m (2 vCPU) 
- Memory requests: 2Gi
- Memory limits: 3Gi (adjusted for ML workload requirements)
- Fluent-bit sidecar: 50m CPU request, 100m limit; 64Mi memory request, 128Mi limit

### ✅ Rule 02 - Pod Security Baseline
- `runAsNonRoot: true` - Prevents root execution
- `seccompProfile.type: RuntimeDefault` - Applies secure computing profile
- `readOnlyRootFilesystem: true` - Locks filesystem
- `capabilities.drop: ["ALL"]` - Drops dangerous capabilities
- Applied to both main container and fluent-bit sidecar

### ✅ Rule 03 - Immutable, Trusted Images
- Uses pinned image with SHA digest: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730`
- Fluent-bit from approved registry: `quay.io/redhat-openshift-approved/fluent-bit:2.1.10@sha256:...`
- No `:latest` tags
- Images from approved internal registry and Red Hat approved registry

### ✅ Rule 04 - Naming & Label Conventions
- Release name: `pe-eng-credit-scoring-prod`
- Mandatory labels applied to all resources:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### ✅ Rule 05 - Logging & Observability
- Prometheus annotations configured:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
  - `prometheus.io/path: "/actuator/prometheus"`
- JSON logs output to stdout via Spring Boot
- Metrics exposed on port 8080 at `/actuator/prometheus` endpoint
- Fluent-bit sidecar for log shipping to OpenShift Loki stack

### ✅ Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness`
  - Initial delay: 60s, period: 30s, timeout: 10s, failure threshold: 3
- Readiness probe: `/actuator/health/readiness`
  - Initial delay: 30s, period: 10s, timeout: 5s, failure threshold: 3
- Startup probe: `/actuator/health/liveness`
  - Initial delay: 30s, period: 10s, timeout: 5s, failure threshold: 30
- Proper timing configuration for JVM applications

## Deployment Files

- `namespace.yaml` - Credit scoring namespace with proper labels
- `serviceaccount.yaml` - Service account for the application (from remote)
- `deployment.yaml` - Main application deployment with 4 replicas and fluent-bit sidecar
- `service.yaml` - ClusterIP service exposing port 8080 with Prometheus annotations
- `configmap.yaml` - Application configuration and ML models configuration
- `fluent-bit-configmap.yaml` - Fluent-bit configuration for log shipping (from remote)
- `ingress.yaml` - External access via nginx ingress
- `networkpolicy.yaml` - Network security policy
- `README.md` - This documentation

## Deployment Commands

```bash
# Apply all manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n credit-scoring -l app.kubernetes.io/name=credit-scoring-engine

# View logs
kubectl logs -n credit-scoring -l app.kubernetes.io/name=credit-scoring-engine

# Access health endpoint
kubectl port-forward -n credit-scoring svc/pe-eng-credit-scoring-prod-service 8080:8080
curl http://localhost:8080/actuator/health/detailed

# Check Prometheus metrics
curl http://localhost:8080/actuator/prometheus
```

## Migration from Cloud Foundry

This k8s deployment maintains feature parity with the original Cloud Foundry `manifest.yml`:
- Same environment variables and configuration
- Same health check endpoints (`/actuator/health/detailed`)
- Adjusted resource allocation (3GB memory limit for ML workload requirements)
- Same external service dependencies (referenced via environment variables)
- Same routing configuration via ingress (credit-scoring.internal.banking.com, credit-api-v3.banking.com)
- Added fluent-bit sidecar for centralized logging compliance

## Security Features

- Non-root execution (UID 1001)
- Read-only root filesystem with writable /tmp volume
- All Linux capabilities dropped
- Runtime default seccomp profile
- No privilege escalation allowed
- Dedicated service account with minimal permissions
- Network policy for ingress/egress control

## Observability Features

- Structured JSON logging to stdout
- Prometheus metrics on `/actuator/prometheus` endpoint
- Automatic service discovery via annotations
- Centralized log aggregation via fluent-bit sidecar
- Health probes for liveness and readiness detection
