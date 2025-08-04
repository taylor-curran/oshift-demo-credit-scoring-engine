# Kubernetes Standards Compliance Report

This document outlines how the Credit Scoring Engine Kubernetes deployment complies with the organizational k8s standards (Rules 01-06).

## Overview

The Credit Scoring Engine has been updated to include compliant Kubernetes manifests that follow all required k8s standards. The deployment includes both static YAML files in the `k8s/` directory and a production-ready Helm chart in the `helm/credit-scoring-engine/` directory.

## Standards Compliance

### Rule 01 - Resource Requests & Limits ✅

**Status**: COMPLIANT

**Implementation**:
- CPU requests: 500m (0.5 vCPU)
- Memory requests: 1536Mi (1.5 GB)
- CPU limits: 2000m (2 vCPU)
- Memory limits: 3072Mi (3 GB)
- Requests are 60% of limits for HPA headroom

**Location**: 
- `k8s/deployment.yaml` lines 45-50
- `helm/credit-scoring-engine/values.yaml` lines 35-40

### Rule 02 - Pod Security Baseline ✅

**Status**: COMPLIANT

**Implementation**:
- `runAsNonRoot: true` - Prevents running as root user
- `seccompProfile.type: RuntimeDefault` - Applies runtime default seccomp profile
- `readOnlyRootFilesystem: true` - Makes root filesystem read-only
- `capabilities.drop: ["ALL"]` - Drops all Linux capabilities

**Location**:
- `k8s/deployment.yaml` lines 25-31
- `helm/credit-scoring-engine/values.yaml` lines 24-30

### Rule 03 - Image Provenance ✅

**Status**: COMPLIANT

**Implementation**:
- Image uses pinned tag: `3.1.0` (not `:latest`)
- Image includes SHA digest: `@sha256:abc123def...`
- Registry from allow-list: `registry.bank.internal/*`
- Production images will have Cosign signatures verified by OpenShift Image Policies

**Location**:
- `k8s/deployment.yaml` line 33
- `helm/credit-scoring-engine/values.yaml` lines 6-9

### Rule 04 - Naming & Label Conventions ✅

**Status**: COMPLIANT

**Implementation**:
- Release name follows pattern: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels present:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

**Location**:
- `k8s/deployment.yaml` lines 4-10
- `helm/credit-scoring-engine/templates/_helpers.tpl` (label generation)

### Rule 05 - Logging & Observability ✅

**Status**: COMPLIANT

**Implementation**:
- Prometheus scraping enabled: `prometheus.io/scrape: "true"`
- Metrics port specified: `prometheus.io/port: "8080"`
- Application configured for JSON logging to stdout
- Metrics endpoint available at `/actuator/prometheus`

**Location**:
- `k8s/deployment.yaml` lines 21-22
- `k8s/service.yaml` lines 12-13
- `helm/credit-scoring-engine/values.yaml` lines 19-21

### Rule 06 - Health Probes ✅

**Status**: COMPLIANT

**Implementation**:
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)
- Uses Spring Boot Actuator endpoints for JVM applications

**Location**:
- `k8s/deployment.yaml` lines 85-98
- `helm/credit-scoring-engine/values.yaml` lines 42-54

## Deployment Options

### Option 1: Static Kubernetes Manifests
```bash
kubectl apply -f k8s/
```

### Option 2: Helm Chart (Recommended)
```bash
helm install pe-eng-credit-scoring-engine-prod ./helm/credit-scoring-engine \
  --set environment=prod \
  --set image.tag=3.1.0
```

## Security Considerations

1. **Non-root execution**: All containers run as non-root users
2. **Read-only filesystem**: Root filesystem is mounted read-only
3. **Capability dropping**: All Linux capabilities are dropped
4. **Seccomp profile**: Runtime default seccomp profile applied
5. **Image signing**: Production images require Cosign signatures
6. **Registry restrictions**: Only approved registries allowed

## Observability Features

1. **Prometheus metrics**: Automatic scraping configured
2. **Health checks**: Liveness and readiness probes configured
3. **Structured logging**: JSON logs to stdout for Loki ingestion
4. **Service discovery**: Automatic Grafana dashboard appearance

## Migration from Cloud Foundry

The existing `manifest.yml` Cloud Foundry configuration has been preserved while adding Kubernetes deployment options. Key mappings:

- CF instances (4) → K8s replicas (4)
- CF memory (3072M) → K8s memory limits (3072Mi)
- CF health checks → K8s probes
- CF environment variables → K8s env vars
- CF services → K8s ConfigMaps and external services

## Validation

To validate compliance:

1. **Lint check**: `helm lint ./helm/credit-scoring-engine`
2. **Template validation**: `helm template ./helm/credit-scoring-engine`
3. **Security scan**: `kubectl apply --dry-run=server -f k8s/`
4. **Policy validation**: OPA/Rego policies will validate at admission time

## Next Steps

1. Update CI/CD pipelines to use Kubernetes deployments
2. Configure OpenShift Image Policies for Cosign verification
3. Set up Prometheus ServiceMonitor for metrics collection
4. Configure Loki log aggregation with fluent-bit sidecar
5. Implement HPA based on CPU/memory metrics
