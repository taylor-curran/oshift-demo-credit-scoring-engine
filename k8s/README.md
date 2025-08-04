# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that are compliant with internal k8s standards (Rules 01-04).

## Standards Compliance

### Rule 01 - Resource Limits ✅
- All containers have CPU and memory requests and limits defined
- Main container: 1200m CPU request, 2000m CPU limit, 1800Mi memory request, 2Gi memory limit
- Follows the rule of thumb: requests ≈ 60% of limits for HPA headroom

### Rule 02 - Security Context ✅
- `runAsNonRoot: true` set at both pod and container level
- `readOnlyRootFilesystem: true` for immutable containers
- `capabilities.drop: ["ALL"]` to drop dangerous capabilities
- `seccompProfile.type: RuntimeDefault` for secure computing
- Non-root user (1001) with proper group settings

### Rule 03 - Image Provenance ✅
- Images use SHA256 digests for immutability
- Images sourced from approved registry: `registry.bank.internal/*`
- No `:latest` tags used

### Rule 04 - Naming & Labels ✅
- Consistent naming convention: `pe-eng-credit-scoring-engine-prod`
- All mandatory labels present:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

## Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n credit-scoring -l app.kubernetes.io/name=credit-scoring-engine

# View logs
kubectl logs -n credit-scoring -l app.kubernetes.io/name=credit-scoring-engine

# Access health endpoint
kubectl port-forward -n credit-scoring svc/pe-eng-credit-scoring-engine-prod 8080:8080
curl http://localhost:8080/actuator/health/detailed
```

## Migration from Cloud Foundry

This k8s deployment maintains feature parity with the original Cloud Foundry `manifest.yml`:
- Same environment variables and configuration
- Same health check endpoints (`/actuator/health/detailed`)
- Adjusted resource allocation (2GB memory limit for k8s standards compliance)
- Same external service dependencies
- Same routing configuration via ingress
