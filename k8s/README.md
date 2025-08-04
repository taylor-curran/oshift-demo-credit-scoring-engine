# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s standards library rules.

## Standards Compliance

### Rule 02 - Security Context Baseline ✅
- `runAsNonRoot: true` - All containers run as non-root user (UID 1001)
- `seccompProfile.type: RuntimeDefault` - Uses runtime default seccomp profile
- `readOnlyRootFilesystem: true` - Root filesystem is read-only
- `capabilities.drop: ["ALL"]` - All Linux capabilities are dropped

### Rule 03 - Image Provenance ✅
- Uses pinned image tag: `registry.bank.internal/credit-scoring-engine:3.1.0`
- Image from approved internal registry: `registry.bank.internal`
- No `:latest` tags used

### Rule 04 - Naming & Label Conventions ✅
- Mandatory labels applied to all resources:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: banking-platform`
  - `environment: prod`
  - `managed-by: kubernetes`

### Rule 05 - Logging & Observability ✅
- Prometheus scraping enabled with annotations:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
  - `prometheus.io/path: "/actuator/prometheus"`
- JSON structured logging via Spring Boot Actuator

### Rule 06 - Health Probes ✅
- Liveness probe: `/actuator/health/liveness`
- Readiness probe: `/actuator/health/readiness`
- Proper timeouts and failure thresholds configured

## Resource Requirements
- CPU requests: 500m, limits: 2000m
- Memory requests: 2Gi, limits: 3Gi
- Matches Cloud Foundry configuration (3GB memory, 4 instances)

## Deployment
```bash
kubectl apply -k k8s/
```

## Files
- `deployment.yaml` - Main application deployment
- `service.yaml` - ClusterIP service for internal access
- `configmap.yaml` - Application configuration
- `networkpolicy.yaml` - Network security policies
- `kustomization.yaml` - Kustomize configuration
