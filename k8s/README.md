# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests for the Credit Scoring Engine that comply with all organizational k8s standards.

## Standards Compliance

### ✅ Rule 01 - Resource Requests & Limits
- CPU requests: 1800m (60% of 3000m limit)
- Memory requests: 1843Mi (60% of 3072Mi limit)
- CPU limits: 3000m
- Memory limits: 3072Mi

### ✅ Rule 02 - Pod Security Baseline
- `runAsNonRoot: true` (container level)
- `seccompProfile.type: RuntimeDefault` (container level)
- `readOnlyRootFilesystem: true` (container level)
- `capabilities.drop: ["ALL"]` (container level)

### ✅ Rule 03 - Image Provenance
- Uses pinned image tag: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:abc123def456789`
- No `:latest` tags
- Uses trusted internal registry

### ✅ Rule 04 - Naming & Label Conventions
- Proper naming: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: openshift`

### ✅ Rule 05 - Logging & Observability
- Prometheus scraping annotations:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
- Metrics endpoint exposed on port 8080
- JSON structured logging format for stdout logs

### ✅ Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)

## Deployment

```bash
# Apply all manifests
kubectl apply -k k8s/

# Or apply individually
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## Configuration

The application configuration is managed through:
- **ConfigMap**: `pe-eng-credit-scoring-engine-prod-config` - Application properties
- **Secret**: `pe-eng-credit-scoring-engine-prod-secrets` - Sensitive credentials
- **Environment Variables**: Defined in deployment.yaml

## Security

- Runs as non-root user with read-only root filesystem
- All capabilities dropped for enhanced security
- Sensitive data stored in Kubernetes secrets (use environment variable substitution)
- Uses trusted internal registry images only

### Secret Management

**IMPORTANT**: Secrets are NOT included in this repository for security reasons.

Use the `secret-template.yaml` file as a reference to create your own secrets:

1. **Manual approach**:
   ```bash
   cp k8s/secret-template.yaml k8s/secret.yaml
   # Edit secret.yaml with actual values
   # Add secret.yaml to .gitignore
   kubectl apply -f k8s/secret.yaml
   ```

2. **External Secret Management** (Recommended):
   - External Secrets Operator
   - HashiCorp Vault
   - AWS Secrets Manager
   - Azure Key Vault

Required secret keys:
- `DB_USERNAME` - Database username
- `DB_PASSWORD` - Database password  
- `REDIS_PASSWORD` - Redis password
- `EXPERIAN_API_KEY` - Experian API key
- `EQUIFAX_API_KEY` - Equifax API key
- `TRANSUNION_API_KEY` - TransUnion API key
