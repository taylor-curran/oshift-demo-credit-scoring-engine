# K8s Standards Compliance Audit and Fixes

This PR implements comprehensive Kubernetes standards compliance fixes for the credit scoring engine application based on the k8s-standards-library Rules 02-06.

## Standards Compliance Assessment

### ✅ Rule 02 - Security Context Compliance
- **runAsNonRoot**: `true` - Prevents running as root user
- **seccompProfile.type**: `RuntimeDefault` - Applies runtime default seccomp profile
- **readOnlyRootFilesystem**: `true` - Makes root filesystem read-only
- **capabilities.drop**: `["ALL"]` - Drops all Linux capabilities

### ✅ Rule 03 - Image Provenance Compliance
- **No :latest tags**: Using pinned version `3.1.0` with SHA digest
- **Registry allow-list**: Using approved `registry.bank.internal`
- **SHA digest pinning**: `@sha256:7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730`

### ✅ Rule 04 - Naming and Labels Compliance
- **Mandatory labels**: All required labels present
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`
- **Release-name prefix**: `pe-eng-credit-scoring-engine-prod` follows `<team>-<app>-<env>` pattern

### ✅ Rule 05 - Logging and Observability Compliance
- **Prometheus annotations**: 
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
  - `prometheus.io/path: "/actuator/prometheus"`
- **JSON logging**: Configured structured logging pattern
- **Metrics exposure**: Spring Boot Actuator endpoints enabled

### ✅ Rule 06 - Health Probes Compliance
- **Liveness probe**: `/actuator/health/liveness` with 30s initial delay
- **Readiness probe**: `/actuator/health/readiness` with 10s initial delay
- **Proper timeouts**: Configured appropriate timeout and failure thresholds

## Changes Made

### New Kubernetes Manifests
- `k8s/deployment.yaml` - Main application deployment with full security context
- `k8s/service.yaml` - Service with proper labels and Prometheus annotations
- `k8s/configmap.yaml` - Configuration with JSON logging setup
- `k8s/secret.yaml` - Secrets with proper labeling
- `k8s/ml-models-configmap.yaml` - ML models configuration

### Resource Configuration
- **CPU requests/limits**: 500m/2000m for proper resource management
- **Memory requests/limits**: 1536Mi/2048Mi optimized for JVM workload
- **Volume mounts**: Proper read-only and writable volume configurations

## Testing
- ✅ All Maven tests pass successfully
- ✅ Spring Boot application starts correctly
- ✅ All k8s manifests validated against standards Rules 02-06

## Migration from Cloud Foundry
This PR represents the migration from Cloud Foundry (manifest.yml) to Kubernetes deployment with full standards compliance.

---

**Link to Devin run**: https://app.devin.ai/sessions/20242264d04f4301b00a74bb36285434  
**Requested by**: @taylor-curran
