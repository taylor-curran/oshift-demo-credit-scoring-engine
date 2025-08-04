# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes deployment manifests that comply with the k8s-standards-library requirements.

## Standards Compliance

### Rule 02 - Security Context ✅
- ✅ `runAsNonRoot: true` - All containers run as non-root user (UID 1001)
- ✅ `seccompProfile.type: RuntimeDefault` - Runtime default seccomp profile applied
- ✅ `readOnlyRootFilesystem: true` - Root filesystem is read-only
- ✅ `capabilities.drop: ["ALL"]` - All Linux capabilities dropped

### Rule 03 - Image Provenance ✅
- ✅ No `:latest` tags - Image uses pinned version with SHA digest
- ✅ Registry allow-list - Uses approved `registry.bank.internal` registry
- ✅ Cosign signatures - Production images verified by OpenShift Image Policies

### Rule 04 - Naming & Labels ✅
- ✅ Mandatory labels applied to all resources:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`
- ✅ Release-name prefix: `pe-eng-credit-scoring-engine-prod`

### Rule 05 - Logging & Observability ✅
- ✅ Prometheus annotations for metrics scraping (`prometheus.io/scrape: "true"`)
- ✅ Prometheus port configuration (`prometheus.io/port: "8080"`)
- ✅ Prometheus path configuration (`prometheus.io/path: "/actuator/prometheus"`)
- ✅ Health probes configured for liveness and readiness
- ✅ Structured logging via Spring Boot Actuator

### Rule 06 - Health Probes ✅
- ✅ Liveness probe: `/actuator/health/liveness` on port 8081
- ✅ Readiness probe: `/actuator/health/readiness` on port 8081
- ✅ Proper timing configuration (initialDelaySeconds, periodSeconds, timeoutSeconds)

## Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/

# Verify deployment
kubectl get pods -n credit-scoring
kubectl get svc -n credit-scoring

# Check application health
kubectl port-forward svc/pe-eng-credit-scoring-engine-prod 8080:8080 -n credit-scoring
curl http://localhost:8080/actuator/health
```

## Resources

- **CPU**: 500m requests, 2000m limits
- **Memory**: 2Gi requests, 3Gi limits
- **Replicas**: 4 instances for high availability
- **Health Checks**: Spring Boot Actuator endpoints on port 8081
- **Security**: Non-root user, read-only filesystem, dropped capabilities

## Important Notes

⚠️ **Image Digest**: The SHA256 digest in deployment.yaml is a placeholder and must be replaced with the actual digest of your built image before deployment.

⚠️ **Security Constraints**: The strict security settings (read-only filesystem, non-root user) may require application modifications if it attempts to write temporary files or logs to the filesystem.

## Testing Locally

Before deploying to Kubernetes, test the application locally:

```bash
# Run tests
mvn test

# Start application
mvn spring-boot:run

# Test endpoints
curl http://localhost:8080/actuator/health
curl http://localhost:8080/actuator/health/liveness
curl http://localhost:8080/actuator/health/readiness
```
