# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s standards library requirements.

## Standards Compliance

### Rule 02 - Security Context Baseline ✅
- `runAsNonRoot: true` - All containers run as non-root user (1001)
- `seccompProfile.type: RuntimeDefault` - Applied at pod and container level
- `readOnlyRootFilesystem: true` - Root filesystem is read-only
- `capabilities.drop: ["ALL"]` - All Linux capabilities dropped
- `allowPrivilegeEscalation: false` - Privilege escalation disabled

### Rule 03 - Image Provenance ✅
- Image uses pinned tag with SHA digest: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- Registry from approved allowlist: `registry.bank.internal/*`
- No `:latest` tags used

### Rule 04 - Naming & Label Conventions ✅
- Release name follows pattern: `pe-eng-credit-scoring-engine-prod` (`<team>-<app>-<env>`)
- All mandatory labels present:
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
- Spring Boot Actuator endpoints exposed for monitoring

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness`
- Readiness probe: `/actuator/health/readiness`
- Appropriate timeouts and failure thresholds configured

### Additional Best Practices ✅
- Resource requests and limits defined
- Network policies for security isolation
- Pod disruption budget for high availability
- Horizontal pod autoscaler for scaling
- Proper volume mounts for writable directories

## Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/

# Verify deployment
kubectl get pods -n credit-scoring
kubectl get svc -n credit-scoring
```

## Monitoring

The application exposes metrics at `/actuator/prometheus` and health checks at:
- `/actuator/health/liveness` - Liveness probe
- `/actuator/health/readiness` - Readiness probe
- `/actuator/health/detailed` - Detailed health information
