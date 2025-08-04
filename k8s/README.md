# Kubernetes Deployment Guide

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine in compliance with k8s standards.

## Standards Compliance

This deployment follows the k8s-standards-library rules:

### Rule 01 - Resource Limits
- ✅ CPU requests: 500m, limits: 2000m
- ✅ Memory requests: 1536Mi, limits: 3072Mi
- ✅ Proper resource allocation for ML workloads

### Rule 02 - Pod Security Baseline
- ✅ `runAsNonRoot: true`
- ✅ `seccompProfile.type: RuntimeDefault`
- ✅ `readOnlyRootFilesystem: true`
- ✅ `capabilities.drop: ["ALL"]`

### Rule 03 - Image Provenance
- ✅ Pinned image tags with SHA digests
- ✅ Registry allow-list: `registry.bank.internal/*`
- ✅ Cosign signature verification (handled by OpenShift Image Policies)

### Rule 04 - Naming & Labels
- ✅ Mandatory labels: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/part-of`, `environment`, `managed-by`
- ✅ Release-name prefix: `pe-eng-credit-scoring-engine-prod`

### Rule 05 - Logging & Observability
- ✅ JSON structured logging via logstash-logback-encoder
- ✅ Prometheus metrics on port 8080 at `/actuator/prometheus`
- ✅ Annotations: `prometheus.io/scrape: "true"`, `prometheus.io/port: "8080"`

### Rule 06 - Health Probes
- ✅ Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- ✅ Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)

## Deployment

### Prerequisites
- Kubernetes cluster with OpenShift or equivalent
- Access to `registry.bank.internal`
- Namespace `retail-banking` created

### Quick Deploy
```bash
# Apply all manifests
kubectl apply -f k8s/

# Or use Helm (recommended)
helm install credit-scoring-engine ./helm/credit-scoring-engine \
  --namespace retail-banking \
  --create-namespace
```

### Verification
```bash
# Check deployment status
kubectl get pods -n retail-banking -l app.kubernetes.io/name=credit-scoring-engine

# Check health endpoints
kubectl port-forward -n retail-banking svc/pe-eng-credit-scoring-engine-prod 8080:8080
curl http://localhost:8080/actuator/health
curl http://localhost:8080/actuator/prometheus

# Check logs (should be JSON formatted)
kubectl logs -n retail-banking -l app.kubernetes.io/name=credit-scoring-engine
```

## Configuration

The application uses ConfigMap for configuration. Key settings:

- **Health Probes**: Spring Boot Actuator endpoints enabled
- **Metrics**: Prometheus metrics exported at `/actuator/prometheus`
- **Logging**: JSON structured logging for production
- **Security**: Non-root user, read-only filesystem, dropped capabilities

## Monitoring

The deployment includes:
- Prometheus scraping annotations
- Health check endpoints for liveness/readiness
- Structured JSON logging for log aggregation
- Resource limits for proper scheduling

## Security

Security features implemented:
- Non-root container execution
- Read-only root filesystem
- All Linux capabilities dropped
- Seccomp profile applied
- Service account with minimal permissions
