# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with all k8s standards rules:

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080  
- `configmap.yaml` - Application configuration and properties
- `ingress.yaml` - External routing for banking domains
- `kustomization.yaml` - Kustomize configuration for deployment management

## K8s Standards Compliance

### Rule 01 - Resource Requests & Limits ✅
- CPU requests: 1800m (60% of 3000m limit)
- Memory requests: 1843Mi (60% of 3072Mi limit)
- Proper resource isolation for multi-tenant clusters

### Rule 02 - Pod Security Baseline ✅
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`

### Rule 03 - Immutable, Trusted Images ✅
- Pinned image tag: `registry.bank.internal/credit-scoring-engine:3.1.0`
- SHA256 digest for immutability
- Trusted internal registry

### Rule 04 - Naming & Label Conventions ✅
- Release name: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/part-of`, `environment`, `managed-by`

### Rule 05 - Logging & Observability ✅
- Prometheus annotations: `prometheus.io/scrape: "true"`, `prometheus.io/port: "8080"`
- Structured JSON logging to stdout

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)

## Deployment

```bash
# Apply all manifests
kubectl apply -k .

# Or apply individually
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f configmap.yaml
kubectl apply -f ingress.yaml
```

## Secrets Management

Database and Redis credentials should be managed separately using:
- External secret management systems (e.g., HashiCorp Vault)
- Kubernetes External Secrets Operator
- Cloud provider secret management services

Refer to your organization's security policies for proper secret management procedures.
