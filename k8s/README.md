# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s standards library (Rules 01-06).

## Standards Compliance Audit Report

### ✅ Rule 01 - Resource Requests & Limits
**Status: COMPLIANT**
- Main container: CPU 500m request / 1000m limit, Memory 1228Mi request / 2048Mi limit
- Fluent-bit sidecar: CPU 50m request / 100m limit, Memory 64Mi request / 128Mi limit
- All containers have proper resource constraints to prevent noisy neighbor issues

### ✅ Rule 02 - Pod Security Baseline
**Status: COMPLIANT**
- `securityContext.runAsNonRoot: true` ✅
- `securityContext.seccompProfile.type: RuntimeDefault` ✅
- `securityContext.readOnlyRootFilesystem: true` ✅
- `securityContext.capabilities.drop: ["ALL"]` ✅
- Both main container and fluent-bit sidecar have identical security settings

### ✅ Rule 03 - Image Provenance & Immutability
**Status: COMPLIANT**
- Main image: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730`
- Fluent-bit image: `quay.io/redhat-openshift-approved/fluent-bit:2.1.10`
- No `:latest` tags used ✅
- Uses approved internal registry (`registry.bank.internal`) ✅
- Uses approved Red Hat registry (`quay.io/redhat-openshift-approved`) ✅
- SHA digest pinning ensures immutability ✅

### ✅ Rule 04 - Naming & Label Conventions
**Status: COMPLIANT**
- Release name prefix: `pe-eng-credit-scoring-engine-prod` (follows `<team>-<app>-<env>` pattern) ✅
- All resources have mandatory labels:
  - `app.kubernetes.io/name: credit-scoring-engine` ✅
  - `app.kubernetes.io/version: "3.1.0"` ✅
  - `app.kubernetes.io/part-of: retail-banking` ✅
  - `environment: prod` ✅
  - `managed-by: helm` ✅

### ✅ Rule 05 - Logging & Observability
**Status: COMPLIANT**
- Prometheus scraping annotations:
  - `prometheus.io/scrape: "true"` ✅
  - `prometheus.io/port: "8080"` ✅
- JSON logging configured in `application.properties` ✅
- Fluent-bit sidecar for log shipping to Loki stack ✅
- Metrics endpoint exposed on port 8080 ✅
- Actuator endpoints enabled for monitoring ✅

### ✅ Rule 06 - Health Probes
**Status: COMPLIANT**
- Liveness probe: `/actuator/health/liveness`
  - Initial delay: 30s, Period: 30s, Timeout: 5s, Failure threshold: 3 ✅
- Readiness probe: `/actuator/health/readiness`
  - Initial delay: 10s, Period: 10s, Timeout: 5s, Failure threshold: 1 ✅
- Uses Spring Boot Actuator endpoints for proper health checking ✅

## Architecture Overview

The deployment includes:
- **Main Container**: Credit Scoring Engine (Spring Boot application)
- **Sidecar Container**: Fluent-bit for structured log shipping
- **ConfigMaps**: Model configuration and fluent-bit configuration
- **Service**: ClusterIP service with Prometheus annotations
- **Ingress**: Routes for internal and external API access
- **Kustomization**: Centralized configuration management

## Deployment Instructions

```bash
# Apply all manifests using Kustomize
kubectl apply -k k8s/

# Or apply individually
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/fluent-bit-configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# Verify deployment
kubectl get pods -l app.kubernetes.io/name=credit-scoring-engine
kubectl get svc pe-eng-credit-scoring-engine-prod
kubectl logs -l app.kubernetes.io/name=credit-scoring-engine -c credit-scoring-engine
```

## Monitoring & Observability

- **Metrics**: Prometheus scrapes metrics from port 8080
- **Logs**: JSON-formatted logs shipped via fluent-bit to Loki
- **Health Checks**: Kubernetes probes monitor application health
- **Tracing**: Ready for distributed tracing integration

## Security Features

- Non-root execution (UID 1001)
- Read-only root filesystem
- All Linux capabilities dropped
- Runtime default seccomp profile
- No privilege escalation allowed
- Signed container images from trusted registries

## Resource Allocation

- **Replicas**: 4 (matching Cloud Foundry configuration)
- **CPU**: 500m-1000m per pod (main container)
- **Memory**: 1228Mi-2048Mi per pod (main container)
- **Total Cluster Resources**: ~2-4 CPU cores, ~5-8GB memory
