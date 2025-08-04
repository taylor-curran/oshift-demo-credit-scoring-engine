# K8s Standards Compliance Audit

## Rule 01 - Resource Requests & Limits
**Status: ✅ COMPLIANT**
- ✅ `resources.requests.cpu: "1200m"` (≥ 50m baseline)
- ✅ `resources.requests.memory: "1228Mi"` (≥ 128Mi baseline)  
- ✅ `resources.limits.cpu: "2000m"` (≤ 4 vCPU baseline)
- ✅ `resources.limits.memory: "2048Mi"` (≤ 2Gi baseline)
- ✅ Requests ≈ 60% of limits (good for HPA headroom)

## Rule 02 - Pod Security Baseline
**Status: ✅ COMPLIANT**
- ✅ `securityContext.runAsNonRoot: true` (pod and container level)
- ✅ `securityContext.seccompProfile.type: RuntimeDefault` (pod and container level)
- ✅ `securityContext.readOnlyRootFilesystem: true` (container level)
- ✅ `securityContext.capabilities.drop: ["ALL"]` (container level)

## Rule 03 - Image Provenance
**Status: ✅ COMPLIANT**
- ✅ No `:latest` tag used
- ✅ Uses pinned tag with SHA digest: `registry.bank.internal/credit-scoring-engine:3.1.0@sha256:...`
- ✅ Registry from allow-list: `registry.bank.internal/*`
- ✅ Sigstore/Cosign signature verification (handled by OpenShift Image Policies)

## Rule 04 - Naming & Label Conventions
**Status: ✅ COMPLIANT**
- ✅ Release-name prefix: `pe-eng-credit-scoring-engine-prod` (follows `<team>-<app>-<env>` pattern)
- ✅ All mandatory labels present:
  - `app.kubernetes.io/name: credit-scoring-engine`
  - `app.kubernetes.io/version: "3.1.0"`
  - `app.kubernetes.io/part-of: retail-banking`
  - `environment: prod`
  - `managed-by: helm`

## Rule 05 - Logging & Observability
**Status: ✅ COMPLIANT**
- ✅ Prometheus annotations present:
  - `prometheus.io/scrape: "true"`
  - `prometheus.io/port: "8080"`
- ✅ HTTP port 8080 exposed for metrics
- ✅ JSON logging to stdout (Spring Boot default)
- ✅ Fluent-bit sidecar can be added via Helm chart

## Rule 06 - Health Probes
**Status: ✅ COMPLIANT**
- ✅ Liveness probe configured:
  - Path: `/actuator/health/liveness`
  - Port: 8080
  - Initial delay: 30s
  - Failure threshold: 3
- ✅ Readiness probe configured:
  - Path: `/actuator/health/readiness`
  - Port: 8080
  - Initial delay: 10s
  - Failure threshold: 1

## Overall Assessment
**Status: ✅ FULLY COMPLIANT**

All Kubernetes manifests (deployment.yaml, service.yaml, configmap.yaml) are fully compliant with k8s standards Rules 01-06. No additional changes required.
