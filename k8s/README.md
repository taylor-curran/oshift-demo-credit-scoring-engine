# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests that are compliant with k8s standards (Rules 01-06).

## Standards Compliance

### ✅ Rule 02 - Security Context
- `runAsNonRoot: true` - Prevents running as root user
- `seccompProfile.type: RuntimeDefault` - Applies secure system call filtering
- `readOnlyRootFilesystem: true` - Makes root filesystem read-only
- `capabilities.drop: ["ALL"]` - Drops all Linux capabilities

### ✅ Rule 03 - Image Provenance
- Uses pinned tag with SHA256 digest (no `:latest`)
- Image from approved registry: `registry.bank.internal`
- **⚠️ Important**: Update SHA256 digest with actual value when image is built

### ✅ Rule 04 - Naming & Labels
- All mandatory labels present:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### ✅ Rule 05 - Logging & Observability
- Prometheus annotations for metrics scraping:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`

### ✅ Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness`
- Readiness probe: `/actuator/health/readiness`

## Resource Allocation (Rule 01)
- **CPU**: 500m requests, 2000m limits
- **Memory**: 1536Mi requests, 3072Mi limits
- **Replicas**: 4 instances for high availability

## Deployment Instructions

1. **Update image digest**: Replace the SHA256 digest in `deployment.yaml` with the actual digest from your built image
2. **Apply manifests**:
   ```bash
   kubectl apply -f namespace.yaml
   kubectl apply -f configmap.yaml
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   ```
3. **Verify deployment**:
   ```bash
   kubectl get pods -n credit-scoring
   kubectl logs -n credit-scoring -l app.kubernetes.io/name=credit-scoring-engine
   ```

## Security Notes

- Application runs as non-root user with minimal privileges
- Root filesystem is read-only (writable volumes mounted for `/tmp` and `/models`)
- All dangerous Linux capabilities are dropped
- Secure system call filtering enabled via seccomp
