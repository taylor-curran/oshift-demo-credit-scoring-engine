# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with enterprise k8s standards for the Credit Scoring Engine application.

## Standards Compliance

### ✅ Rule 01 - Resource Limits & Requests
- CPU requests: 1200m, limits: 2000m (60% ratio)
- Memory requests: 1536Mi, limits: 3072Mi (50% ratio)
- Follows recommended request-to-limit ratio for HPA headroom

### ✅ Rule 02 - Pod Security Baseline
- `runAsNonRoot: true` with user ID 1001
- `readOnlyRootFilesystem: true` with writable tmp/logs volumes
- `seccompProfile.type: RuntimeDefault`
- `capabilities.drop: ["ALL"]` - all dangerous capabilities dropped

### ✅ Rule 03 - Immutable, Trusted Images
- Pinned image with SHA256 digest (no `:latest` tags)
- Uses approved registry: `registry.bank.internal/*`
- Image: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730`

### ✅ Rule 04 - Naming & Label Conventions
- Release name: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

### ✅ Rule 05 - Logging & Observability
- JSON structured logging to stdout with custom pattern
- Prometheus metrics annotations on pods and services
- Fluent-bit sidecar for log shipping to Loki stack
- Metrics endpoint exposed on port 8080 with `/metrics` path

### ✅ Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness` on port 8081
- Readiness probe: `/actuator/health/readiness` on port 8081
- Startup probe: `/actuator/health/readiness` on port 8081
- Proper timing configuration for JVM applications

## Deployment Files

- `namespace.yaml` - Dedicated namespace with proper labels
- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service for internal/actuator communication
- `configmap.yaml` - Environment variables and ML model configuration
- `secrets.yaml` - Sensitive configuration (API keys, database credentials)
- `ingress.yaml` - External access routing with TLS
- `kustomization.yaml` - Kustomize configuration for deployment management
- `README.md` - This documentation

## Deployment Commands

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

Check deployment status:
```bash
kubectl get pods -n credit-scoring
kubectl logs -f deployment/pe-eng-credit-scoring-engine-prod -n credit-scoring
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

## Logging & Observability

### Structured Logging
- Application outputs JSON logs to stdout using custom logback pattern
- Fluent-bit sidecar collects logs and forwards to Loki stack
- Log format includes timestamp, level, thread, logger, message, and MDC context

### Metrics
- Prometheus metrics exposed on port 8080 at `/metrics` endpoint
- Pod and service annotations enable automatic scraping
- Fluent-bit metrics available on port 2020

## Migration from Cloud Foundry

This Kubernetes deployment maintains feature parity with the original Cloud Foundry manifest.yml:
- 4 application instances → 4 pod replicas
- 3GB memory allocation → 3072Mi memory limit
- Health check endpoint → liveness/readiness probes
- Environment variables → configmaps and secrets
- External routes → ingress configuration
- CF services → K8s secrets and external service references
