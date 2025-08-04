# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine application in compliance with k8s standards.

## Standards Compliance

All manifests in this directory comply with the following k8s standards:

### Rule 01 - Resource Requests & Limits
- All containers have CPU and memory requests and limits defined
- Requests are set to ~60% of limits for HPA headroom
- Baseline: CPU ≥ 50m, Memory ≥ 128Mi

### Rule 02 - Pod Security Baseline
- `runAsNonRoot: true` - All containers run as non-root user (1001)
- `seccompProfile.type: RuntimeDefault` - Secure computing profile enabled
- `readOnlyRootFilesystem: true` - Filesystem is read-only
- `capabilities.drop: ["ALL"]` - All dangerous capabilities dropped

### Rule 03 - Immutable, Trusted Images
- No `:latest` tags used
- All images use pinned SHA digests
- Images sourced from internal registry: `registry.bank.internal/*`

### Rule 04 - Naming & Label Conventions
- Release name format: `banking-eng-credit-scoring-engine-{env}`
- All resources include mandatory labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: dev|prod`
  - `managed-by: helm`

## Files

- `namespace.yaml` - Credit scoring namespace
- `deployment.yaml` - Main production deployment
- `deployment-dev.yaml` - Development deployment with logging sidecar
- `deployment-prod.yaml` - Production deployment with logging sidecar
- `service-dev.yaml` - Development service
- `service-prod.yaml` - Production service
- `configmap.yaml` - ML models configuration
- `fluent-bit-configmap-dev.yaml` - Development logging configuration
- `fluent-bit-configmap-prod.yaml` - Production logging configuration

## Deployment

Apply manifests in order:
1. `kubectl apply -f namespace.yaml`
2. `kubectl apply -f configmap.yaml`
3. `kubectl apply -f fluent-bit-configmap-*.yaml`
4. `kubectl apply -f deployment-*.yaml`
5. `kubectl apply -f service-*.yaml`

## Monitoring

Prometheus metrics are available at `/metrics` endpoint on port 8080 for all deployments.
