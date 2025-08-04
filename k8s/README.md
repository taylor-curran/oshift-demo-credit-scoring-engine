# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine application that comply with enterprise k8s standards (Rules 02-06).

## Standards Compliance

### ✅ Rule 01 - Resource Requests & Limits
- CPU requests: 500m (0.5 vCPU)
- CPU limits: 2000m (2 vCPU) 
- Memory requests: 1536Mi (~75% of limits)
- Memory limits: 2Gi (compliant with ≤2Gi standard)

### ✅ Rule 02 - Pod Security Baseline
- `runAsNonRoot: true` - All containers run as non-root user (1001)
- `seccompProfile.type: RuntimeDefault` - Seccomp profile applied at pod and container level
- `readOnlyRootFilesystem: true` - Root filesystem is read-only
- `capabilities.drop: ["ALL"]` - All Linux capabilities dropped
- `allowPrivilegeEscalation: false` - Prevents privilege escalation

### ✅ Rule 03 - Image Provenance
- No `:latest` tags used - All images pinned to specific versions
- Registry allowlist enforced - Only `registry.bank.internal/*` images used
- Cosign signature verification handled by OpenShift Image Policies
- Uses pinned image: `registry.bank.internal/credit-scoring-engine:3.1.0`
- Fluent-bit sidecar: `registry.bank.internal/fluent-bit:2.1.0`

### ✅ Rule 04 - Naming & Label Conventions
- Release name prefix: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels present on all resources:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### ✅ Rule 05 - Logging & Observability
- Prometheus annotations for metrics scraping:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
  - `prometheus.io/path: "/actuator/prometheus"`
- JSON structured logging configured via Spring Boot (logback-spring.xml)
- Fluent-bit sidecar for log forwarding to Loki stack
- Automatic Grafana dashboard discovery

### ✅ Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 30s period, 10s timeout)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 10s period, 5s timeout)
- Proper failure thresholds configured (3 failures for liveness, 1 for readiness)

## Deployment Files

- `deployment.yaml` - Main application deployment with 4 replicas and full security compliance
- `service.yaml` - ClusterIP service exposing port 8080 with Prometheus annotations
- `configmap.yaml` - ML models configuration
- `ingress.yaml` - External access via nginx ingress
- `fluent-bit-sidecar.yaml` - Enhanced deployment with logging sidecar
- `networkpolicy.yaml` - Network security policies
- `README.md` - This documentation

## Deployment Commands

```bash
# Apply all manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -l app.kubernetes.io/name=credit-scoring-engine

# View logs
kubectl logs -l app.kubernetes.io/name=credit-scoring-engine

# Access health endpoint
kubectl port-forward svc/pe-eng-credit-scoring-engine-prod 8080:8080
curl http://localhost:8080/actuator/health/detailed

# Check Prometheus metrics
curl http://localhost:8080/actuator/prometheus
```

## Monitoring & Observability

The application exposes metrics at `/actuator/prometheus` on port 8080 and will automatically appear in Grafana dashboards via Prometheus auto-discovery.

Logs are structured as JSON and forwarded to the OpenShift Loki stack via fluent-bit sidecar for centralized log aggregation.

## Migration from Cloud Foundry

This k8s deployment maintains feature parity with the original Cloud Foundry `manifest.yml`:
- Same environment variables and configuration
- Same health check endpoints (`/actuator/health/detailed`)
- Adjusted resource allocation (2GB memory limit for k8s standards compliance)
- Same external service dependencies
- Enhanced security with k8s standards compliance
- Improved observability with structured logging and metrics
