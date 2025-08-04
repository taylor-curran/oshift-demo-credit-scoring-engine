# K8s Standards Verification Checklist

## Pre-Deployment Verification

### Rule 02 - Security Context
- [ ] Verify `runAsNonRoot: true` is set at pod and container level
- [ ] Confirm `seccompProfile.type: RuntimeDefault` is configured
- [ ] Check `readOnlyRootFilesystem: true` for all containers
- [ ] Validate `capabilities.drop: ["ALL"]` is applied
- [ ] Test that containers start successfully with security constraints

### Rule 03 - Image Provenance  
- [ ] Confirm no `:latest` tags are used in any image references
- [ ] Verify all images use approved registries (registry.bank.internal, quay.io/redhat-openshift-approved)
- [ ] Check that main application image uses SHA digest pinning
- [ ] Validate image signatures if Cosign verification is enabled

### Rule 04 - Naming & Labels
- [ ] Verify all mandatory labels are present on all resources:
  - `app.kubernetes.io/name`
  - `app.kubernetes.io/version` 
  - `app.kubernetes.io/part-of`
  - `environment`
  - `managed-by`
- [ ] Check resource names follow `<team>-<app>-<env>` pattern
- [ ] Confirm label consistency across deployment, service, ingress, configmaps

### Rule 05 - Logging & Observability
- [ ] Verify Prometheus scraping annotations are present
- [ ] Check fluent-bit sidecar is configured for log forwarding
- [ ] Confirm JSON logging is enabled in application configuration
- [ ] Test that metrics endpoint is accessible on specified port

### Rule 06 - Health Probes
- [ ] Verify liveness probe is configured with appropriate endpoint
- [ ] Check readiness probe has reasonable timing settings
- [ ] Confirm probe endpoints return proper HTTP status codes
- [ ] Test probe behavior during application startup and shutdown

## Deployment Testing
- [ ] Apply manifests to test cluster: `kubectl apply -k k8s/`
- [ ] Verify all pods start successfully
- [ ] Check resource allocation matches requests/limits
- [ ] Test ingress routing to application endpoints
- [ ] Validate health probe endpoints respond correctly
- [ ] Confirm logs are being forwarded to Loki
- [ ] Verify Prometheus is scraping metrics

## Security Validation
- [ ] Run security scanning on deployed pods
- [ ] Verify no privileged containers are running
- [ ] Check that file system is read-only where expected
- [ ] Confirm network policies are enforced (if applicable)

## Performance Testing
- [ ] Load test application with current resource limits
- [ ] Monitor resource usage during peak load
- [ ] Verify autoscaling behavior (if HPA is configured)
- [ ] Check application performance meets SLA requirements
