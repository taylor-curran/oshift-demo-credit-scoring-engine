# Kubernetes Configurations for Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine application with full compliance to k8s standards.

## K8s Standards Compliance

All configurations in this directory comply with the following k8s standards:

### Rule 01 - Resource Requests & Limits ✅
- All containers have proper CPU and memory requests and limits
- Main container: 200m-1000m CPU, 1228Mi-2048Mi memory
- Fluent-bit sidecar: 50m-100m CPU, 64Mi-128Mi memory

### Rule 02 - Pod Security Baseline ✅
- `runAsNonRoot: true` for all containers
- `readOnlyRootFilesystem: true` for enhanced security
- `seccompProfile.type: RuntimeDefault` for syscall filtering
- `capabilities.drop: ["ALL"]` to remove dangerous capabilities
- `allowPrivilegeEscalation: false` to prevent privilege escalation

### Rule 03 - Immutable, Trusted Images ✅
- No `:latest` tags used
- All images use pinned SHA256 digests
- Images sourced from approved registries:
  - `registry.bank.internal/*` for main application
  - `quay.io/redhat-openshift-approved/*` for fluent-bit

### Rule 04 - Naming & Label Conventions ✅
- Consistent naming pattern: `pe-eng-credit-scoring-engine-prod`
- All resources include mandatory labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

## Deployment

Deploy using Kustomize:
```bash
kubectl apply -k k8s/
```

Or deploy individual manifests:
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/fluent-bit-configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

## Health Checks

The application includes comprehensive health probes:
- Liveness probe: `/actuator/health/liveness` on port 8081
- Readiness probe: `/actuator/health/readiness` on port 8081

## Security Features

- Non-root execution (UID 1001)
- Read-only root filesystem with writable `/tmp` volume
- Dropped all Linux capabilities
- Seccomp runtime default profile
- No privilege escalation allowed
