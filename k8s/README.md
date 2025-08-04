# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests that comply with the k8s-standards-library rules 01-06.

## Standards Compliance

### Rule 01 - Resource Requests & Limits
- ✅ CPU requests: 1200m (main), 50m (sidecar)
- ✅ Memory requests: 1843Mi (main), 64Mi (sidecar)
- ✅ CPU limits: 2000m (main), 100m (sidecar)
- ✅ Memory limits: 3072Mi (main), 128Mi (sidecar)
- ✅ Requests are ~60% of limits for HPA headroom

### Rule 02 - Pod Security Baseline
- ✅ runAsNonRoot: true
- ✅ runAsUser: 1001, runAsGroup: 1001, fsGroup: 1001
- ✅ seccompProfile.type: RuntimeDefault
- ✅ readOnlyRootFilesystem: true
- ✅ capabilities.drop: ["ALL"]
- ✅ allowPrivilegeEscalation: false

### Rule 03 - Immutable, Trusted Images
- ✅ Pinned image tags with SHA digests
- ✅ registry.bank.internal allow-listed registry
- ✅ No :latest tags used

### Rule 04 - Naming & Label Conventions
- ✅ Mandatory labels: app.kubernetes.io/name, app.kubernetes.io/version, app.kubernetes.io/part-of, environment, managed-by
- ✅ Release-name prefix: pe-eng-credit-scoring-engine-prod

### Rule 05 - Logging & Observability
- ✅ Prometheus annotations for metrics scraping
- ✅ Fluent-bit sidecar for JSON log shipping to Loki
- ✅ Structured logging configuration
- ✅ Metrics endpoint at `/actuator/prometheus`

### Rule 06 - Health Probes
- ✅ Liveness probe: /actuator/health/liveness
- ✅ Readiness probe: /actuator/health/readiness
- ✅ Startup probe configured for JVM applications
- ✅ Proper timeouts and failure thresholds

## Deployment

```bash
# Apply all manifests
kubectl apply -k .

# Or apply individually
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f ml-models-configmap.yaml
kubectl apply -f fluent-bit-configmap.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f networkpolicy.yaml
```

## Migration from Cloud Foundry

These manifests replace the `manifest.yml` Cloud Foundry configuration with equivalent Kubernetes resources:

- **Applications** → Deployment with 4 replicas
- **Memory/Disk** → Resource requests/limits
- **Environment variables** → ConfigMaps and container env vars
- **Services** → Kubernetes Services and ConfigMaps
- **Routes** → Ingress resources (see ingress.yaml)
- **Health checks** → Liveness/Readiness probes

## Monitoring

The application exposes metrics at `/actuator/prometheus` on port 8080 and is automatically discovered by Prometheus via annotations.

## Security

- All containers run as non-root user (1001)
- Read-only root filesystem with temporary volumes for writable areas
- Network policies restrict ingress/egress traffic
- Seccomp profiles applied for syscall filtering
