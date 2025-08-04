# Credit Scoring Engine Helm Chart

This Helm chart deploys the Credit Scoring Engine application following k8s-standards compliance.

## Standards Compliance

This chart implements the following k8s-standards:

- **Rule 01 - Resource Limits**: CPU and memory requests/limits defined
- **Rule 02 - Security Context**: runAsNonRoot, seccomp, readOnlyRootFilesystem, capabilities drop
- **Rule 03 - Image Provenance**: Uses pinned tags from approved registry
- **Rule 04 - Naming & Labels**: Mandatory labels for discoverability and cost allocation
- **Rule 05 - Logging & Observability**: Prometheus annotations and JSON logging
- **Rule 06 - Health Probes**: Liveness and readiness probes configured

## Installation

```bash
helm install credit-scoring-engine ./helm \
  --set image.tag=3.1.0 \
  --set labels.environment=prod
```

## Configuration

Key configuration options:

- `replicaCount`: Number of application instances (default: 4)
- `resources.limits.memory`: Memory limit (default: 3Gi)
- `resources.requests.cpu`: CPU request (default: 1200m)
- `extraCaps`: Additional Linux capabilities if needed
- `labels.environment`: Environment label (dev/test/prod)

## Security

The chart enforces Pod Security Baseline standards:
- Runs as non-root user (UID 1001)
- Read-only root filesystem
- Drops all Linux capabilities
- Uses RuntimeDefault seccomp profile
