# Complete K8s Standards Compliance Implementation

This PR implements comprehensive Kubernetes standards compliance for the credit scoring engine application, addressing all required standards (Rules 02-06).

## Changes Made

### ✅ Rule 02 - Pod Security Baseline
- Added `runAsNonRoot: true` at both pod and container level
- Configured `seccompProfile.type: RuntimeDefault`
- Enabled `readOnlyRootFilesystem: true`
- Dropped all capabilities with `capabilities.drop: ["ALL"]`

### ✅ Rule 03 - Image Provenance
- Replaced mutable tags with pinned versions using SHA256 digests
- Used approved internal registry `registry.bank.internal`
- No `:latest` tags in any manifests

### ✅ Rule 04 - Naming & Label Conventions
- Applied proper naming convention: `pe-eng-credit-scoring-engine-prod`
- Added all mandatory labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: openshift`

### ✅ Rule 05 - Logging & Observability
- Added Prometheus annotations: `prometheus.io/scrape: "true"`, `prometheus.io/port: "8080"`
- Configured JSON logging format in application properties
- Implemented fluent-bit sidecar for log shipping to OpenShift Loki

### ✅ Rule 06 - Health Probes
- Configured liveness probe: `/actuator/health/liveness`
- Configured readiness probe: `/actuator/health/readiness`
- Proper timing and failure thresholds set

## Files Added/Modified

- `k8s/deployment.yaml` - Main application deployment with security contexts and probes
- `k8s/service.yaml` - Service with proper labels and Prometheus annotations
- `k8s/configmap.yaml` - Application configuration with JSON logging
- `k8s/fluent-bit-configmap.yaml` - Fluent-bit configuration for log shipping
- `k8s/README.md` - Documentation of standards compliance

## Testing

- ✅ Maven tests pass: `mvn test`
- ✅ All k8s standards compliance verified
- ✅ Application configuration validated

## Deployment

Deploy with:
```bash
kubectl apply -f k8s/
```

---

**Link to Devin run:** https://app.devin.ai/sessions/25cbbd5f82ed4655a3e36cdf1634b1d1
**Requested by:** @taylor-curran
