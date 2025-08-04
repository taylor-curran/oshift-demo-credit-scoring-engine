# Kubernetes Deployment for Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine application in compliance with organizational k8s standards (Rules 02-06).

## Standards Compliance

### ✅ Rule 02 - Pod Security Baseline
- `runAsNonRoot: true` - Prevents running as root user
- `seccompProfile.type: RuntimeDefault` - Applies secure system call filtering
- `readOnlyRootFilesystem: true` - Makes container filesystem immutable
- `capabilities.drop: ["ALL"]` - Removes all Linux capabilities

### ✅ Rule 03 - Image Provenance
- Uses pinned image tag with SHA256 digest: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- Sources from approved internal registry: `registry.bank.internal`
- Image signing verification handled by OpenShift Image Policies

### ✅ Rule 04 - Naming & Labels
All resources include mandatory labels:
- `app.kubernetes.io/name: credit-scoring-engine`
- `app.kubernetes.io/version: "3.1.0"`
- `app.kubernetes.io/part-of: retail-banking`
- `environment: prod`
- `managed-by: openshift`

Release name follows convention: `pe-eng-credit-scoring-engine-prod`

### ✅ Rule 05 - Logging & Observability
- `prometheus.io/scrape: "true"` - Enables Prometheus metrics collection
- `prometheus.io/port: "8080"` - Specifies metrics endpoint port
- `prometheus.io/path: "/actuator/prometheus"` - Spring Boot metrics path
- JSON structured logging to stdout for fluent-bit collection

### ✅ Rule 06 - Health Probes
- **Liveness Probe**: `/actuator/health/liveness` - Detects application deadlock
- **Readiness Probe**: `/actuator/health/readiness` - Controls traffic routing
- Proper timeouts and failure thresholds configured

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - ML model configuration and metadata
- `route.yaml` - OpenShift routes for external access
- `networkpolicy.yaml` - Network security policies

## Deployment

```bash
# Apply all manifests
kubectl apply -f k8s/

# Verify deployment
kubectl get pods -l app.kubernetes.io/name=credit-scoring-engine
kubectl get svc pe-eng-credit-scoring-engine-prod
```

## Monitoring

The application exposes metrics at `/actuator/prometheus` and will be automatically discovered by Prometheus due to the scraping annotations.

Health checks are available at:
- `/actuator/health/liveness`
- `/actuator/health/readiness`
- `/actuator/health/detailed`

## Security

- All containers run as non-root with read-only filesystems
- Network policies restrict ingress/egress traffic
- Seccomp profiles applied for system call filtering
- All Linux capabilities dropped for minimal attack surface
