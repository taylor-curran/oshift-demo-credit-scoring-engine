# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes deployment manifests for the Credit Scoring Engine application, fully compliant with the k8s-standards-library (Rules 01-06).

## Standards Compliance

### ✅ Rule 01 - Resource Requests & Limits
- All containers have CPU/memory requests and limits defined
- Main container: 200m-2000m CPU, 1536Mi-2Gi memory
- Fluent-bit sidecar: 50m-200m CPU, 128Mi-256Mi memory
- Follows 60% request-to-limit ratio for HPA headroom

### ✅ Rule 02 - Pod Security Baseline
- `runAsNonRoot: true` for all containers
- `seccompProfile.type: RuntimeDefault` applied
- `readOnlyRootFilesystem: true` with writable volumes for /tmp and logs
- `capabilities.drop: ["ALL"]` removes dangerous capabilities

### ✅ Rule 03 - Immutable, Trusted Images
- No `:latest` tags - uses pinned version `3.1.0` with SHA digest
- Images from approved registries: `registry.bank.internal/*` and `quay.io/redhat-openshift-approved/*`
- Production images require Cosign signature verification (handled by OpenShift Image Policies)

### ✅ Rule 04 - Naming & Label Conventions
- Release name prefix: `pe-eng-credit-scoring-engine-prod`
- Mandatory labels on all resources:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: kubernetes`

### ✅ Rule 05 - Logging & Observability
- JSON structured logging to stdout (Spring Boot default)
- Fluent-bit sidecar ships logs to OpenShift Loki stack
- Prometheus metrics exposed on port 8080 at `/actuator/prometheus`
- Required annotations: `prometheus.io/scrape: "true"`, `prometheus.io/port: "8080"`
- ServiceMonitor for automatic Prometheus discovery

### ✅ Rule 06 - Health Probes
- Liveness probe: `/actuator/health/liveness` (30s initial delay, 3 failure threshold)
- Readiness probe: `/actuator/health/readiness` (10s initial delay, 1 failure threshold)
- Uses Spring Boot Actuator endpoints for JVM health monitoring

## Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/

# Verify deployment
kubectl get pods -n credit-scoring
kubectl logs -f deployment/pe-eng-credit-scoring-engine-prod -n credit-scoring
```

## Files

- `namespace.yaml` - Dedicated namespace with proper labels
- `deployment.yaml` - Main application deployment with fluent-bit sidecar
- `service.yaml` - ClusterIP service with Prometheus annotations
- `configmap.yaml` - Application configuration (non-sensitive)
- `configmap-fluent-bit.yaml` - Log shipping configuration
- `secret.yaml` - Sensitive API endpoints and credentials
- `hpa.yaml` - Horizontal Pod Autoscaler (4-12 replicas)
- `ingress.yaml` - External access routing
- `servicemonitor.yaml` - Prometheus metrics collection
