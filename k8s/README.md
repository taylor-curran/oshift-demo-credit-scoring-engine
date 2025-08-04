# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with all k8s standards rules (01-06).

## Standards Compliance

### Rule 01 - Resource Limits
- ✅ CPU requests: 500m, limits: 2000m
- ✅ Memory requests: 1536Mi, limits: 3072Mi
- ✅ Requests are ~75% of limits for HPA headroom

### Rule 02 - Security Context
- ✅ runAsNonRoot: true
- ✅ seccompProfile.type: RuntimeDefault
- ✅ readOnlyRootFilesystem: true
- ✅ capabilities.drop: ["ALL"]

### Rule 03 - Image Provenance
- ✅ No :latest tags - using pinned version 3.1.0 with SHA digest
- ✅ Registry allow-list - using registry.bank.internal/*
- ✅ Sigstore/Cosign signature verification (handled by OpenShift Image Policies)

### Rule 04 - Naming & Labels
- ✅ Mandatory labels: app.kubernetes.io/name, app.kubernetes.io/version, app.kubernetes.io/part-of, environment, managed-by
- ✅ Release-name prefix: banking-credit-scoring-prod (team-app-env format)

### Rule 05 - Logging & Observability
- ✅ Prometheus annotations: prometheus.io/scrape: "true", prometheus.io/port: "8080"
- ✅ JSON logging to stdout (configured in application.properties)
- ✅ Metrics endpoint exposed on port 8080

### Rule 06 - Health Probes
- ✅ Liveness probe: /actuator/health/liveness, 30s initial delay, 3 failure threshold
- ✅ Readiness probe: /actuator/health/readiness, 10s initial delay, 1 failure threshold

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Application configuration
- `ingress.yaml` - External access routing
- `README.md` - This documentation

## Deployment

```bash
kubectl apply -f k8s/
```
