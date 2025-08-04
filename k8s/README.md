# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s standards:

## Standards Compliance

### Rule 01 - Resource Limits ✅
- CPU requests: 500m (0.5 vCPU)
- CPU limits: 2000m (2 vCPU) 
- Memory requests: 2Gi
- Memory limits: 3Gi
- Requests are 60% of limits for HPA headroom

### Rule 02 - Security Context ✅
- `runAsNonRoot: true`
- `seccompProfile.type: RuntimeDefault`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ["ALL"]`
- `allowPrivilegeEscalation: false`

### Rule 03 - Image Provenance ✅
- Uses pinned tag with digest: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- No `:latest` tags
- Uses approved internal registry

### Rule 04 - Naming & Labels ✅
- Release name: `pe-eng-credit-scoring-engine-prod`
- Required labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Configuration for ML models

## Migration from Cloud Foundry

These manifests replace the Cloud Foundry `manifest.yml` configuration with equivalent Kubernetes resources that meet enterprise security and operational standards.
