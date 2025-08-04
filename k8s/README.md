# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the organization's K8s standards.

## Standards Compliance

These manifests comply with all required K8s standards:

### Rule 01 - Resource Limits
- All containers have CPU and memory requests and limits defined
- Requests are set to ~60% of limits for HPA headroom
- CPU: 600m request, 1000m limit
- Memory: 1843Mi request, 3072Mi limit

### Rule 02 - Security Context
- `runAsNonRoot: true` - prevents running as root user
- `seccompProfile.type: RuntimeDefault` - applies default seccomp profile
- `readOnlyRootFilesystem: true` - makes root filesystem read-only
- `capabilities.drop: ["ALL"]` - drops all Linux capabilities

### Rule 03 - Image Provenance
- Uses pinned image tag with SHA digest
- Image from approved registry: `registry.bank.internal/*`
- No `:latest` tags used

### Rule 04 - Naming & Labels
- Follows naming convention: `pe-eng-credit-scoring-engine-prod`
- All resources have mandatory labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: openshift`

### Rule 05 - Logging & Observability
- Prometheus scraping annotations added
- Metrics endpoint exposed on port 8080

### Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)

## Deployment

Apply the manifests in order:

```bash
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml
```

## Resources

- **Namespace**: `credit-scoring`
- **Deployment**: 4 replicas with 3GB memory limit per pod
- **Service**: ClusterIP service exposing port 8080
- **Ingress**: Routes for internal and external API access
- **ConfigMap**: Application configuration
