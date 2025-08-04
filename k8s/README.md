# Kubernetes Manifests for Credit Scoring Engine

This directory contains Kubernetes manifests for deploying the Credit Scoring Engine application to OpenShift/Kubernetes clusters.

## Files

- `deployment.yaml` - Main application deployment with 4 replicas
- `service.yaml` - ClusterIP service exposing port 8080
- `configmap.yaml` - Configuration data for the application

## Resource Configuration

### CPU and Memory
- **CPU Requests**: 600m (0.6 vCPU)
- **CPU Limits**: 1000m (1.0 vCPU)
- **Memory Requests**: 1843Mi (~1.8 GB)
- **Memory Limits**: 3072Mi (~3.0 GB)

### Security Context
The deployment follows banking security standards:
- Runs as non-root user (UID 1001)
- Read-only root filesystem
- All capabilities dropped
- Runtime default seccomp profile
- No privilege escalation allowed

### Health Checks
- **Startup Probe**: `/actuator/health` (initial startup)
- **Liveness Probe**: `/actuator/health/liveness` (container health)
- **Readiness Probe**: `/actuator/health/readiness` (traffic readiness)

### Observability
- Prometheus metrics exposed on port 8080 at `/actuator/prometheus`
- Automatic service discovery via annotations

## Deployment

```bash
kubectl apply -f k8s/
```

## Standards Compliance

These manifests comply with all banking k8s standards:
- ✅ Rule 01: Resource limits and requests
- ✅ Rule 02: Security context baseline
- ✅ Rule 03: Image provenance (pinned SHA, approved registry)
- ✅ Rule 04: Naming and labeling conventions
- ✅ Rule 05: Logging and observability
- ✅ Rule 06: Health probes
