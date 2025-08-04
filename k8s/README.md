# Kubernetes Manifests - Standards Compliance

This directory contains Kubernetes manifests for the Credit Scoring Engine that comply with all required K8s standards.

## Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
- **CPU requests**: 600m (60% of 1000m limit)
- **Memory requests**: 1843Mi (60% of 3072Mi limit)
- **CPU limits**: 1000m
- **Memory limits**: 3072Mi (matching Cloud Foundry 3GB allocation)

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

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Configuration for ML models
- `ingress.yaml` - External access routing

## Migration from Cloud Foundry

This configuration migrates the application from Cloud Foundry (manifest.yml) to Kubernetes while maintaining:
- Same memory allocation (3GB)
- Same replica count (4 instances)
- Same environment variables
- Same health check endpoints
- Same external routes
