# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s standards (Rules 01-06).

## Standards Compliance

### Rule 01 - Resource Limits
- ✅ CPU requests: 500m, limits: 2000m
- ✅ Memory requests: 1536Mi, limits: 3072Mi
- ✅ Follows 60% request-to-limit ratio for HPA headroom

### Rule 02 - Security Context
- ✅ `runAsNonRoot: true`
- ✅ `seccompProfile.type: RuntimeDefault`
- ✅ `readOnlyRootFilesystem: true`
- ✅ `capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance
- ✅ Uses pinned image with SHA256 digest
- ✅ Registry from approved allow-list: `registry.bank.internal/*`
- ✅ No `:latest` tags

### Rule 04 - Naming & Labels
- ✅ Mandatory labels: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/part-of`, `environment`, `managed-by`
- ✅ Consistent naming convention with kustomize management
- ✅ All resources properly labeled for discoverability

### Rule 05 - Logging & Observability
- ✅ Prometheus annotations: `prometheus.io/scrape: "true"`, `prometheus.io/port: "8080"`
- ✅ Structured JSON logging configured in application.properties
- ✅ Metrics endpoint on port 8080
- ✅ Fluent-bit sidecar for log shipping to OpenShift Loki stack

### Rule 06 - Health Probes
- ✅ Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- ✅ Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)

## Deployment

### Deploy
```bash
# Apply all manifests
kubectl apply -k k8s/

# Or apply individually
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### Security Note
In production environments, use external secret management solutions like:
- Kubernetes External Secrets Operator
- HashiCorp Vault
- AWS Secrets Manager
- Azure Key Vault
- Google Secret Manager

## Files

- `deployment.yaml` - Main application deployment with 4 replicas and fluent-bit sidecar
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Application configuration with JSON structured logging
- `fluent-bit-configmap.yaml` - Log shipping configuration for OpenShift Loki stack
- Database configured to use H2 in-memory for demo (use external secret management for production databases)
- `kustomization.yaml` - Kustomize configuration for environment-specific deployments
