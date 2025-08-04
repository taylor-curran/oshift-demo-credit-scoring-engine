# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with all k8s standards rules (01-04):

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080  
- `configmap.yaml` - Application configuration and properties
- `ingress.yaml` - External routing for banking domains
- `hpa.yaml` - Horizontal Pod Autoscaler (4-12 replicas)
- `secret-template.yaml` - Template for creating secrets (replace placeholders with actual values)
- `kustomization.yaml` - Kustomize configuration for deployment management

## K8s Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
- CPU requests: 1800m (60% of 3000m limit)
- Memory requests: 1843Mi (60% of 3072Mi limit)
- Proper resource isolation for multi-tenant clusters

### Rule 02 - Pod Security Baseline ✅
- `runAsNonRoot: true` with specific user/group IDs (1001)
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`
- `allowPrivilegeEscalation: false`

### Rule 03 - Immutable, Trusted Images ✅
- Pinned image tag: `registry.bank.internal/credit-scoring-engine:3.1.0`
- SHA256 digest for immutability: `@sha256:a1b2c3d4e5f6...`
- Trusted internal registry

### Rule 04 - Naming & Label Conventions ✅
- Release name: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/part-of`, `environment`, `managed-by`

### Additional Features ✅
- Prometheus annotations: `prometheus.io/scrape: "true"`, `prometheus.io/port: "8080"`
- Health probes: liveness (`/actuator/health/liveness`) and readiness (`/actuator/health/readiness`)
- Horizontal Pod Autoscaler for dynamic scaling

## Deployment

```bash
# Apply all manifests using Kustomize
kubectl apply -k .

# Or apply individually
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f configmap.yaml
kubectl apply -f ingress.yaml
kubectl apply -f hpa.yaml

# Check deployment status
kubectl get pods -l app.kubernetes.io/name=credit-scoring-engine

# View logs
kubectl logs -l app.kubernetes.io/name=credit-scoring-engine
```

## Secrets Management

**Note**: The secret-template.yaml file contains placeholder values. Replace these with actual values before deployment.

Database and Redis credentials should be managed separately using:
- Copy secret-template.yaml to secret.yaml and replace all REPLACE_WITH_* placeholders
- External secret management systems (e.g., HashiCorp Vault)
- Kubernetes External Secrets Operator
- Cloud provider secret management services
- Never commit actual secrets to the repository

Refer to your organization's security policies for proper secret management procedures.

## Migration from Cloud Foundry

This replaces the Cloud Foundry `manifest.yml` with equivalent Kubernetes resources:
- 4 instances → 4 replicas with HPA scaling (4-12 replicas)
- 3072M memory → 3072Mi memory limit
- Environment variables → ConfigMap with application.properties
- Routes → Ingress with banking domain routing
- Health checks → Liveness/Readiness probes
