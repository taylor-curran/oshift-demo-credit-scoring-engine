# Kubernetes Deployment Guide

This directory contains Kubernetes manifests for the Credit Scoring Engine that are fully compliant with k8s standards.

## Files

- `deployment.yaml` - Main application deployment with security context, resource limits, and health probes
- `service.yaml` - ClusterIP service with Prometheus annotations for observability
- `configmap.yaml` - Application configuration properties
- `secrets.yaml` - Secret templates for database and Redis credentials

## Standards Compliance

All manifests comply with the following k8s standards:

- **Rule 01**: Resource requests and limits configured
- **Rule 02**: Security context with runAsNonRoot, seccomp, readOnlyRootFilesystem, capabilities drop
- **Rule 03**: Pinned image tags with SHA digest from approved registry
- **Rule 04**: Mandatory labels and proper naming conventions
- **Rule 05**: Prometheus scrape annotations for observability
- **Rule 06**: Liveness and readiness probes with Spring Boot Actuator

## Deployment

### Prerequisites

Before deploying, you need to set the following environment variables for secrets:

```bash
export DATABASE_URL="postgresql://your-db-host:5432/creditdb"
export DATABASE_USERNAME="your-db-user"
export DATABASE_PASSWORD="your-db-password"
export REDIS_HOST="your-redis-host"
export REDIS_PORT="6379"
```

### Deploy

```bash
# Apply all manifests
kubectl apply -f k8s/

# Or apply individually
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### Verify Deployment

```bash
# Check pod status
kubectl get pods -l app.kubernetes.io/name=credit-scoring-engine

# Check service
kubectl get svc banking-credit-scoring-engine-service

# Check health endpoints
kubectl port-forward svc/banking-credit-scoring-engine-service 8080:8080
curl http://localhost:8080/actuator/health
```
