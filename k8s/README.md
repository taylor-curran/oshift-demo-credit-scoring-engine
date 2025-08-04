# Kubernetes Manifests - Standards Compliance

This directory contains Kubernetes manifests for the Credit Scoring Engine that comply with all required K8s standards.

## Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
**Main Container (credit-scoring-engine):**
- **CPU requests**: 500m (25% of 2000m limit)
- **Memory requests**: 1536Mi (75% of 2Gi limit)
- **CPU limits**: 2000m
- **Memory limits**: 2Gi

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

## Deployment Files

- `deployment.yaml` - Main application deployment with 4 replicas + fluent-bit sidecar
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Configuration for ML models
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
