# Kubernetes Deployment

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine to a Kubernetes cluster.

## Files

- `deployment.yaml` - Main application deployment with security contexts and resource limits
- `service.yaml` - ClusterIP service exposing the application
- `configmap.yaml` - Configuration for ML models
- `fluent-bit-configmap.yaml` - Configuration for fluent-bit logging sidecar
- `ingress.yaml` - Ingress configuration for external access
- `kustomization.yaml` - Kustomize configuration for managing all resources

## Deployment

```bash
# Apply all manifests
kubectl apply -k k8s/

# Or apply individually
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/ingress.yaml
```

## K8s Standards Compliance

All manifests are compliant with k8s standards Rules 01-04:

- **Rule 01**: Resource requests and limits defined for all containers
- **Rule 02**: Security contexts with runAsNonRoot, readOnlyRootFilesystem, and capabilities dropped
- **Rule 03**: Pinned image tags from trusted registries (no :latest)
- **Rule 04**: Proper naming conventions and mandatory labels

## Resource Limits

- CPU: 500m request, 1000m limit
- Memory: 1228Mi request, 2048Mi limit
- Replicas: 4 (matching Cloud Foundry configuration)

## Health Probes

- Liveness: `/actuator/health/liveness`
- Readiness: `/actuator/health/readiness`
