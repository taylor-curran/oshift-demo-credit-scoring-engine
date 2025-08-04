# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine application following enterprise k8s standards.

## Standards Compliance

This deployment follows all required k8s standards:

### Rule 01 - Resource Requests & Limits
- CPU requests: 500m, limits: 2000m
- Memory requests: 1536Mi, limits: 3072Mi
- Requests set to ~60% of limits for HPA headroom

### Rule 02 - Pod Security Baseline
- `runAsNonRoot: true` with user ID 1001
- `readOnlyRootFilesystem: true` with writable volumes for tmp/logs
- `seccompProfile.type: RuntimeDefault`
- `capabilities.drop: ["ALL"]` - all dangerous capabilities dropped

### Rule 03 - Immutable, Trusted Images
- Uses pinned image with SHA256 digest (no :latest tags)
- Registry: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- Complies with internal registry allow-list

### Rule 04 - Naming & Label Conventions
- Release name: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/part-of`, `environment`, `managed-by`

## Deployment

Deploy using kustomize:
```bash
kubectl apply -k k8s/
```

Or deploy individual manifests:
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

## Configuration

### Secrets
Update `secrets.yaml` with actual values for:
- Database credentials
- API keys for credit bureaus
- Encryption keys

### Environment-specific Changes
For different environments (dev/test/prod), update:
- Namespace name
- Resource limits
- Replica count
- Ingress hostnames
- Environment label values

## Health Checks

The application exposes health endpoints on port 8081:
- Liveness: `/actuator/health/liveness`
- Readiness: `/actuator/health/readiness`
- Detailed: `/actuator/health/detailed`

## Migration from Cloud Foundry

This replaces the Cloud Foundry `manifest.yml` deployment with Kubernetes-native resources:
- CF services → K8s secrets and external service references
- CF routes → K8s ingress
- CF health checks → K8s probes
- CF environment variables → K8s configmaps and secrets
