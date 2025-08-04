# Kubernetes Manifests - Standards Compliance

This directory contains Kubernetes manifests for the Credit Scoring Engine that comply with all required K8s standards.

## Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
**Main Container (credit-scoring-engine):**
- **CPU requests**: 500m (25% of 2000m limit)
- **Memory requests**: 1536Mi (51% of 3Gi limit)
- **CPU limits**: 2000m
- **Memory limits**: 3Gi

**Sidecar Container (fluent-bit):**
- **CPU requests**: 50m (50% of 100m limit)
- **Memory requests**: 64Mi (50% of 128Mi limit)
- **CPU limits**: 100m
- **Memory limits**: 128Mi

### Rule 02 - Pod Security Baseline ✅
- **runAsNonRoot**: true (user 1001)
- **seccompProfile**: RuntimeDefault
- **readOnlyRootFilesystem**: true
- **capabilities**: drop ALL
- **allowPrivilegeEscalation**: false

### Rule 03 - Immutable, Trusted Images ✅
- **No :latest tags**: Uses pinned version `3.1.0`
- **Registry compliance**: Uses `registry.bank.internal/*`
- **SHA256 digest**: Includes image digest for immutability

### Rule 04 - Naming & Label Conventions ✅
- **Release name**: `pe-eng-credit-scoring-engine-prod`
- **Mandatory labels**:
  - `app.kubernetes.io/name`: credit-scoring-engine
  - `app.kubernetes.io/version`: "3.1.0"
  - `app.kubernetes.io/part-of`: retail-banking
  - `environment`: prod
  - `managed-by`: helm

### Rule 05 - Logging & Observability ✅
- **JSON structured logging**: Configured in application.properties
- **Prometheus metrics**: Exposed on port 8080 with proper annotations
- **Fluent-bit sidecar**: Ships logs to OpenShift Loki stack

### Rule 06 - Health Probes ✅
- **Liveness probe**: `/actuator/health/liveness` with 30s initial delay
- **Readiness probe**: `/actuator/health/readiness` with 10s initial delay

## Deployment Files

- `deployment.yaml` - Main application deployment with 4 replicas + fluent-bit sidecar
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Configuration for application properties and ML models
- `ingress.yaml` - External access routing with TLS
- `namespace.yaml` - Dedicated credit-scoring namespace
- `serviceaccount.yaml` - Service account with automountServiceAccountToken: false
- `fluent-bit-configmap.yaml` - Logging configuration for fluent-bit sidecar

## Migration from Cloud Foundry

This configuration migrates the application from Cloud Foundry (manifest.yml) to Kubernetes while maintaining:
- Same replica count (4 instances)
- Same environment variables and configuration
- Enhanced health check endpoints (liveness/readiness)
- Same external routes with TLS termination
- Added comprehensive logging with fluent-bit sidecar
- Enhanced security with dedicated namespace and service account

## Deployment Commands

```bash
# Apply all manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n credit-scoring -l app.kubernetes.io/name=credit-scoring-engine

# Port forward for testing
kubectl port-forward -n credit-scoring svc/pe-eng-credit-scoring-engine-prod 8080:80

# View logs
kubectl logs -n credit-scoring -l app.kubernetes.io/name=credit-scoring-engine -c credit-scoring-engine

# View fluent-bit logs
kubectl logs -n credit-scoring -l app.kubernetes.io/name=credit-scoring-engine -c fluent-bit
```
