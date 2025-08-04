# Kubernetes Deployment

This directory contains Kubernetes manifests for the Credit Scoring Engine that comply with the k8s standards (Rules 02-06).

## Standards Compliance

### Rule 02 - Security Context
- ✅ `runAsNonRoot: true` (container level)
- ✅ `seccompProfile.type: RuntimeDefault` (container level)
- ✅ `readOnlyRootFilesystem: true` (container level)
- ✅ `capabilities.drop: ["ALL"]` (container level)

### Rule 03 - Image Provenance
- ✅ Pinned image tag with SHA digest: `3.1.0@sha256:7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730`
- ✅ Uses approved registry: `registry.bank.internal`
- ✅ No `:latest` tags

### Rule 04 - Naming & Labels
- ✅ Mandatory labels: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/part-of`, `environment`, `managed-by`
- ✅ Release name prefix: `banking-credit-scoring-engine-prod` (follows `<team>-<app>-<env>` pattern)

### Rule 05 - Logging & Observability
- ✅ Prometheus annotations: `prometheus.io/scrape: "true"`, `prometheus.io/port: "8080"`
- ✅ JSON logging configuration in ConfigMap with structured format
- ✅ Metrics endpoint exposed on port 8080

### Rule 06 - Health Probes
- ✅ Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- ✅ Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)

## Resource Limits
- ✅ CPU requests: 1000m, limits: 2000m
- ✅ Memory requests: 1536Mi, limits: 3072Mi
- ✅ Requests set to ~75% of limits for HPA headroom

## Deployment

### Using kubectl
```bash
kubectl apply -k k8s/
```

### Using kustomize
```bash
kustomize build k8s/ | kubectl apply -f -
```

## Files

- `deployment.yaml` - Main application deployment with security context and resource limits
- `service.yaml` - Service definition with Prometheus annotations
- `configmap.yaml` - Application configuration with JSON logging
- `kustomization.yaml` - Kustomize configuration for environment management
- `README.md` - This documentation

## Security Features

The deployment implements Pod Security Baseline requirements:
- Non-root user execution
- Read-only root filesystem with writable volumes for `/tmp`, `/models`, and `/config`
- Dropped all Linux capabilities
- Runtime default seccomp profile
- Proper resource constraints to prevent resource exhaustion

## Configuration Management

The application uses a ConfigMap for external configuration, allowing for:
- Environment-specific settings without rebuilding images
- JSON structured logging for better observability
- Prometheus metrics exposure for monitoring integration
- Spring Boot Actuator health endpoints for Kubernetes probes
