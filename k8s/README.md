# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the banking organization's k8s standards (Rules 01-04).

## Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
- CPU requests: 500m, limits: 2000m
- Memory requests: 1536Mi, limits: 3072Mi
- Requests set to ~60% of limits for HPA headroom

### Rule 02 - Pod Security Baseline ✅
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### Rule 03 - Immutable, Trusted Images ✅
- Image pinned with digest: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- No `:latest` tags used
- Uses approved internal registry

### Rule 04 - Naming & Label Conventions ✅
- Release name: `pe-eng-credit-scoring-engine-dev`
- Mandatory labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: dev`
  - `managed-by: helm`

## Manifests

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Non-sensitive configuration
- `secret-template.yaml` - Template for creating secrets (replace placeholders with actual values)
- `ingress.yaml` - External access routing
- `hpa.yaml` - Horizontal Pod Autoscaler (4-12 replicas)

## Deployment

**Note**: The secret-template.yaml file contains placeholder values. Replace these with actual values before deployment or use a proper secret management system.

```bash
# Create actual secret from template and apply all manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -l app.kubernetes.io/name=credit-scoring-engine

# View logs
kubectl logs -l app.kubernetes.io/name=credit-scoring-engine
```

### Secret Management
The `secret-template.yaml` file contains placeholder values that must be replaced with actual values:
- Copy secret-template.yaml to secret.yaml and replace all REPLACE_WITH_* placeholders
- Use external secret management tools (e.g., HashiCorp Vault, AWS Secrets Manager)
- Use Kubernetes native secrets created separately from this manifest
- Never commit actual secrets to the repository

## Migration from Cloud Foundry

This replaces the Cloud Foundry `manifest.yml` with equivalent Kubernetes resources:
- 4 instances → 4 replicas with HPA scaling
- 3072M memory → 3072Mi memory limit
- Environment variables → ConfigMap + Secret
- Routes → Ingress
- Health checks → Liveness/Readiness probes
