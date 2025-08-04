# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests that are fully compliant with k8s standards (Rules 01-06).

## Standards Compliance

### ✅ Rule 01 - Resource Requests & Limits
- **CPU requests**: 500m (exceeds 50m minimum requirement)
- **Memory requests**: 1536Mi (exceeds 128Mi minimum requirement)
- **CPU limits**: 2000m (within 4 vCPU maximum)
- **Memory limits**: 3072Mi (appropriate for ML workload)
- **Replicas**: 4 instances for high availability

### ✅ Rule 02 - Pod Security Baseline
- `runAsNonRoot: true` - Prevents running as root user
- `seccompProfile.type: RuntimeDefault` - Applies secure system call filtering
- `readOnlyRootFilesystem: true` - Makes root filesystem read-only
- `capabilities.drop: ["ALL"]` - Drops all dangerous Linux capabilities

### ✅ Rule 03 - Immutable, Trusted Images
- Uses pinned tag with SHA256 digest (no `:latest`)
- Image from approved registry: `registry.bank.internal`
- **⚠️ Important**: Update SHA256 digest with actual value when image is built

### ✅ Rule 04 - Naming & Label Conventions
- All mandatory labels present:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`
- Resource names follow `<team>-<app>-<env>` pattern:
  - Deployment: `banking-credit-scoring-prod`
  - Service: `banking-credit-scoring-service`

## Additional Features

### Observability & Monitoring
- Prometheus annotations for metrics scraping:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`

### ✅ Rule 05 - Logging and Observability
- JSON structured logging to stdout via Spring Boot
- Fluent-bit sidecar for log shipping to Loki stack
- Prometheus annotations for metrics scraping:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`

### ✅ Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness` (Spring Boot Actuator)
- Readiness probe: `/actuator/health/readiness` (Spring Boot Actuator)
- Proper timing configuration for JVM applications

## Deployment Instructions

1. **Update image digest**: Replace the SHA256 digest in `deployment.yaml` with the actual digest from your built image
2. **Apply manifests**:
   ```bash
   kubectl apply -f namespace.yaml
   kubectl apply -f configmap.yaml
   kubectl apply -f fluent-bit-configmap.yaml
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   ```
3. **Verify deployment**:
   ```bash
   kubectl get pods -n credit-scoring
   kubectl logs -n credit-scoring -l app.kubernetes.io/name=credit-scoring-engine
   kubectl get deployment banking-credit-scoring-prod -n credit-scoring
   kubectl get service banking-credit-scoring-service -n credit-scoring
   ```

## Security Notes

- Application runs as non-root user with minimal privileges
- Root filesystem is read-only (writable volumes mounted for `/tmp` and `/models`)
- All dangerous Linux capabilities are dropped
- Secure system call filtering enabled via seccomp

## Compliance Verification

To verify compliance with k8s standards:

```bash
# Check resource limits
kubectl describe deployment banking-credit-scoring-prod -n credit-scoring | grep -A 10 "Limits\|Requests"

# Check security context
kubectl get pod -n credit-scoring -o yaml | grep -A 10 securityContext

# Check labels
kubectl get deployment banking-credit-scoring-prod -n credit-scoring --show-labels

# Check image provenance
kubectl get deployment banking-credit-scoring-prod -n credit-scoring -o jsonpath='{.spec.template.spec.containers[0].image}'
```
