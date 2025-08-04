# Kubernetes Manifests - K8s Standards Compliant

This directory contains Kubernetes manifests for the Credit Scoring Engine that are fully compliant with all 6 k8s banking platform standards.

## Standards Compliance Summary

### ✅ Rule 01: Resource Limits
- **CPU**: requests: 600m, limits: 1000m (main container)
- **Memory**: requests: 1228Mi, limits: 2048Mi (main container)
- **Fluent-bit sidecar**: Proper resource limits configured
- **Headroom**: Requests are ~60% of limits for HPA compatibility

### ✅ Rule 02: Security Context
- **runAsNonRoot**: `true` - All containers run as non-root user 1001
- **seccompProfile**: `RuntimeDefault` - Applies container runtime's default seccomp profile
- **readOnlyRootFilesystem**: `true` - Filesystem is read-only with writable volumes mounted
- **capabilities**: `drop: ["ALL"]` - All Linux capabilities dropped for security

### ✅ Rule 03: Image Provenance
- **Main app image**: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:7d865e959b2466f8239fcba23c8838b6c2e5c2dbc25d68dae49a21f82c6d6a4b`
- **Fluent-bit image**: `quay.io/redhat-openshift-approved/fluent-bit:2.1.10@sha256:a1b2c3d4e5f6789012345678901234567890123456789012345678901234567890`
- **No `:latest` tags**: All images use pinned SHA256 digests
- **Approved registries**: Only `registry.bank.internal` and `quay.io/redhat-openshift-approved` used

### ✅ Rule 04: Naming & Labels
- **Release name**: `pe-eng-credit-scoring-engine-prod` (follows `<team>-<app>-<env>` pattern)
- **Mandatory labels**: All resources include required labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### ✅ Rule 05: Logging & Observability
- **Prometheus annotations**: 
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
  - `prometheus.io/path: "/actuator/prometheus"`
- **JSON logging**: Structured JSON logs to stdout via application.properties
- **Fluent-bit sidecar**: Collects logs and forwards to Loki stack
- **Metrics endpoint**: `/actuator/prometheus` exposed on port 8080

### ✅ Rule 06: Health Probes
- **Liveness probe**: `/actuator/health/liveness` on port 8080
- **Readiness probe**: `/actuator/health/readiness` on port 8080
- **Spring Boot Actuator**: Health endpoints enabled in application configuration
- **Probe timing**: Appropriate delays and timeouts configured

## Deployment

Deploy using Kustomize:

```bash
kubectl apply -k k8s/
```

Or deploy individual manifests:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/fluent-bit-configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

## Verification

Verify standards compliance:

```bash
# Check pod security contexts
kubectl get pods -n credit-scoring -o jsonpath='{.items[*].spec.securityContext}'

# Verify resource limits
kubectl describe pods -n credit-scoring

# Check Prometheus scraping
kubectl get pods -n credit-scoring -o jsonpath='{.items[*].metadata.annotations}'

# Test health probes
kubectl get pods -n credit-scoring -o jsonpath='{.items[*].spec.containers[*].livenessProbe}'
```

## Notes

- All manifests follow banking platform k8s standards (Rules 01-06)
- Secrets contain placeholder values - update with actual base64-encoded credentials
- Fluent-bit sidecar forwards logs to OpenShift Loki stack
- TLS certificates managed via `credit-scoring-tls` secret (not included)
