# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with all k8s standards (Rules 02-06).

## Standards Compliance

### Rule 02 - Security Context Baseline ✅
- `runAsNonRoot: true` - All containers run as non-root user (1001)
- `seccompProfile.type: RuntimeDefault` - Seccomp profile applied
- `readOnlyRootFilesystem: true` - Root filesystem is read-only
- `capabilities.drop: ["ALL"]` - All Linux capabilities dropped

### Rule 03 - Image Provenance ✅
- No `:latest` tags used - All images pinned to specific versions with SHA digests
- Registry allowlist enforced - Only `registry.bank.internal/*` images used
- Cosign signature verification handled by OpenShift Image Policies

### Rule 04 - Naming & Labels ✅
- Release name prefix: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels present on all resources:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### Rule 05 - Logging & Observability ✅
- Prometheus annotations for metrics scraping:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
  - `prometheus.io/path: "/actuator/prometheus"`
- JSON structured logging configured via Spring Boot
- Fluent-bit sidecar for log forwarding to Loki stack

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness` (60s initial delay, 30s period)
- Readiness probe: `/actuator/health/readiness` (30s initial delay, 10s period)
- Proper timeouts and failure thresholds configured

## Files

- `deployment.yaml` - Main application deployment
- `service.yaml` - ClusterIP service for internal access
- `configmap.yaml` - Configuration for ML models
- `fluent-bit-sidecar.yaml` - Enhanced deployment with logging sidecar
- `networkpolicy.yaml` - Network security policies
- `README.md` - This documentation

## Deployment

```bash
kubectl apply -f k8s/
```

## Monitoring

The application exposes metrics at `/actuator/prometheus` on port 8080 and will automatically appear in Grafana dashboards via Prometheus auto-discovery.

Logs are structured as JSON and forwarded to the OpenShift Loki stack via fluent-bit sidecar.
