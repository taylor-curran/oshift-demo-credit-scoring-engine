# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the organization's k8s standards.

## Standards Compliance

### ✅ Rule 01 - Resource Requests & Limits
- **CPU requests**: 300m (0.3 vCPU)
- **CPU limits**: 2000m (2 vCPU) 
- **Memory requests**: 1536Mi (~60% of limits for HPA headroom)
- **Memory limits**: 3072Mi (3GB as per original manifest)

### ✅ Rule 02 - Pod Security Baseline
- **runAsNonRoot**: true
- **seccompProfile**: RuntimeDefault
- **readOnlyRootFilesystem**: true
- **capabilities.drop**: ["ALL"]

### ✅ Rule 03 - Image Provenance
- **Registry**: registry.bank.internal (trusted internal registry)
- **Tag**: Pinned to version 3.1.0 with SHA256 digest
- **No :latest tags**: Compliant with immutable image policy

### ✅ Rule 04 - Naming & Label Conventions
- **Name format**: pe-eng-credit-scoring-engine-prod
- **Mandatory labels**:
  - `app.kubernetes.io/name`: credit-scoring-engine
  - `app.kubernetes.io/version`: "3.1.0"
  - `app.kubernetes.io/part-of`: retail-banking
  - `environment`: prod
  - `managed-by`: openshift

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service for internal communication
- `configmap.yaml` - Non-sensitive configuration and ML model placeholder
- `secret.yaml` - Sensitive credentials (base64 encoded)
- `route.yaml` - OpenShift routes for external access

## Deployment

```bash
kubectl apply -f k8s/
```

## Notes

- The image SHA256 digest is a placeholder and should be updated with the actual digest
- Secret values are base64 encoded placeholders and should be replaced with real credentials
- ML model ConfigMap should be replaced with proper persistent volume in production
- Health check endpoints match the original manifest configuration
