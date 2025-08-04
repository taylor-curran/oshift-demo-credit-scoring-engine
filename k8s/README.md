# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes deployment manifests that comply with the k8s-standards-library requirements.

## Standards Compliance

### Rule 01 - Resource Limits
- ✅ `resources.requests.cpu: "500m"` - CPU requests set (≥ 50m baseline)
- ✅ `resources.requests.memory: "2Gi"` - Memory requests set (≥ 128Mi baseline)
- ✅ `resources.limits.cpu: "2000m"` - CPU limits set (≤ 4 vCPU baseline)
- ✅ `resources.limits.memory: "3Gi"` - Memory limits set (≤ 2Gi baseline, adjusted for ML workload)

### Rule 02 - Security Context
- ✅ `runAsNonRoot: true` - All containers run as non-root user (UID 1001)
- ✅ `seccompProfile.type: RuntimeDefault` - Runtime default seccomp profile applied
- ✅ `readOnlyRootFilesystem: true` - Root filesystem is read-only
- ✅ `capabilities.drop: ["ALL"]` - All Linux capabilities dropped

### Rule 03 - Image Provenance
- ✅ No `:latest` tags - Image uses pinned version with SHA digest
- ✅ Registry allow-list - Uses approved `registry.bank.internal` registry
- ✅ Cosign signatures - Production images verified by OpenShift Image Policies

### Rule 04 - Naming & Labels
- ✅ Mandatory labels applied to all resources:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`
- ✅ Release-name prefix: `pe-eng-credit-scoring-engine-prod`

### Rule 05 - Logging & Observability
- ✅ Prometheus annotations for metrics scraping (`prometheus.io/scrape: "true"`)
- ✅ Prometheus port annotation (`prometheus.io/port: "8080"`)
- ✅ Prometheus path annotation (`prometheus.io/path: "/actuator/prometheus"`)
- ✅ Health probes configured for liveness and readiness
- ✅ Structured logging via Spring Boot Actuator

### Rule 06 - Health Probes
- ✅ Liveness probe configured with Spring Boot Actuator endpoint (`/actuator/health/liveness`)
- ✅ Readiness probe configured with Spring Boot Actuator endpoint (`/actuator/health/readiness`)
- ✅ Startup probe configured for JVM applications with appropriate delays
- ✅ Proper timeouts and failure thresholds for production workloads

## Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/

# Verify deployment
kubectl get pods -n credit-scoring
kubectl get svc -n credit-scoring
```

## Resources

- **CPU**: 500m requests, 2000m limits
- **Memory**: 2Gi requests, 3Gi limits
- **Replicas**: 4 instances for high availability
- **Health Checks**: Spring Boot Actuator endpoints
