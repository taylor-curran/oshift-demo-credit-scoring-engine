# Cloud Foundry to OpenShift Migration Analysis

## Phase 1: Investigation Results

### Artifact Purposes
- **manifest.yml**: Defines CF deployment with 4 instances, 3GB memory, 5GB disk quota, multi-buildpack setup (Java + Python)
- **pom.xml**: Maven build configuration for Spring Boot 2.7.8 application with Java 17
- **application.properties**: Development configuration using H2 in-memory database

### Dependencies & Integrations
- **CF Services**: credit-postgres-primary, credit-postgres-replica, credit-redis-cluster, model-storage-s3, credit-bureau-proxy, encryption-service, audit-trail-kafka
- **External APIs**: Experian, Equifax, TransUnion credit bureaus, The Work Number API, Plaid API
- **Timeouts**: 15-second timeout for external API calls, 20-second health check timeout

### Resource Requirements (from manifest.yml)
- **Instances**: 4 → will become 4 replicas
- **Memory**: 3072M (3GB) → container memory limits
- **Disk**: 5G → persistent volume claims if needed
- **JVM Settings**: -Xmx2560m -XX:+UseG1GC -XX:+UseStringDeduplication

### Kubernetes Resource Calculations (following 01-resource-limits standard)
Based on CF memory allocation of 3GB and JVM heap of 2.5GB for ML operations:
```yaml
resources:
  requests:
    cpu: "1200m"      # 60% of 2000m limit
    memory: "1800Mi"   # 60% of 3Gi limit  
  limits:
    cpu: "2000m"      # Suitable for ML workload
    memory: "3Gi"     # Matches CF allocation
```
- Follows rule: requests ≈ 60% of limits for HPA headroom
- CPU limits ≤ 4 vCPU (compliant with standard)
- Memory limits ≤ 2 Gi standard exceeded due to ML requirements (3Gi needed)

### Build & Deployment Process
- **Current**: `cf push` with Java + Python buildpacks
- **Target**: Docker build + `oc apply` with Kubernetes manifests
- **Build Tool**: Maven with Spring Boot plugin
- **Artifact**: JAR file (credit-scoring-engine-3.1.0.jar)
- **CI/CD**: GitHub Actions workflow (.github/workflows/main.yml) - "Standards Application CI"
  - Automated Devin-based code review against K8s standards
  - Triggers on all pushes for compliance auditing
  - No traditional build/test steps in CI - relies on external review
- **Local Development**: `mvn spring-boot:run` on port 8080 with H2 database
- **Testing**: `mvn test` for unit tests

### Deployment Process Analysis
**Current CF Process:**
1. `mvn clean install` - builds JAR artifact
2. `cf push` - deploys using manifest.yml with Java + Python buildpacks
3. CF automatically provisions services and sets environment variables

**Target OpenShift Process:**
1. `mvn clean install` - build JAR artifact (same as current)
2. `docker build -t credit-scoring-engine:latest .` - create container image
3. `kind load docker-image credit-scoring-engine:latest --name openshift-demo` - load to cluster
4. `oc new-project demo-credit-scoring-engine` - create project
5. `oc apply -f configmap.yaml` - apply configuration
6. `oc apply -f secret.yaml` - apply secrets  
7. `oc apply -f deployment.yaml` - deploy application
8. `oc apply -f service.yaml` - expose service
9. `oc rollout status deployment/credit-scoring-engine` - monitor deployment

### CI/CD Integration Plan
- Current: GitHub Actions calls Devin API for standards review
- Target: Add Docker build step before Devin review
- Maintain: Standards compliance auditing via existing workflow

### Security & Compliance
- **FCRA Compliance**: Enabled (Fair Credit Reporting Act)
- **ECOA Compliance**: Enabled (Equal Credit Opportunity Act)
- **Health Checks**: HTTP endpoint at /actuator/health/detailed
- **Routes**: Internal banking domain routing

### Platform-Specific Features
- **VCAP_SERVICES**: CF service bindings → Kubernetes ConfigMaps/Secrets
- **Multi-buildpack**: Java + Python → Multi-stage Dockerfile
- **CF Routes**: → OpenShift Routes/Ingress
- **CF Health Checks**: → Kubernetes liveness/readiness probes

## Phase 2: Security & Compliance Analysis

### Regulatory Compliance Requirements
- **FCRA Compliance**: Fair Credit Reporting Act - enabled in manifest.yml
  - Requires consent validation before credit checks
  - Mandates adverse action notifications for declined applications
  - Must maintain audit trails for all credit decisions
- **ECOA Compliance**: Equal Credit Opportunity Act - enabled in manifest.yml
  - Prohibits discrimination in credit decisions
  - Requires specific data handling and reporting procedures

### Security Context Requirements (following 02-security-context standard)
Based on financial services security requirements:
```yaml
securityContext:
  runAsNonRoot: true
  seccompProfile:
    type: RuntimeDefault
  readOnlyRootFilesystem: true
  capabilities:
    drop: ["ALL"]
```

### Encryption & Data Protection
- **Encryption Service**: CF service binding → Kubernetes Secret with encryption keys
- **Audit Trail**: Kafka service → Kubernetes logging/monitoring integration
- **Credit Bureau Proxy**: Secure API gateway → Network policies and service mesh

### Health Check Security
- **Endpoint**: `/actuator/health/detailed` - contains sensitive system information
- **Access Control**: Must restrict health endpoint access in production
- **Timeout**: 20-second health check timeout maintained

### Image Provenance Requirements (following 03-image-provenance standard)
For production deployment:
```yaml
# BAD - mutable tag
image: credit-scoring-engine:latest

# GOOD - pinned tag with digest
image: registry.bank.internal/credit-scoring-engine:3.1.0@sha256:abc123...
```

**Requirements:**
- **Tag Pinning**: MUST NOT use `:latest` tag - use specific version tags
- **Registry Allow-list**: Images must originate from:
  - `registry.bank.internal/*` (internal registry)
  - `quay.io/redhat-openshift-approved/*` (approved external)
- **Cosign Signatures**: Production images must have valid Cosign signatures
- **Verification**: Handled by OpenShift Image Policies

### Network Policies & Encryption
- **Encryption at Rest**: Database and S3 storage encryption via CF services → K8s persistent volume encryption
- **Network Policies**: Restrict pod-to-pod communication for credit bureau API access
- **Labels for Compliance**: Required for automated compliance scanning and cost allocation

## Phase 3: Platform-Specific Features Analysis

### VCAP_SERVICES Replacement Strategy
Current CF service bindings → Kubernetes equivalents:
- **credit-postgres-primary/replica** → PostgreSQL StatefulSet with primary/replica configuration
- **credit-redis-cluster** → Redis Operator or Helm chart deployment
- **model-storage-s3** → S3-compatible storage via PVC or external S3 service
- **credit-bureau-proxy** → Kubernetes Service with external endpoints
- **encryption-service** → Kubernetes Secret with encryption keys
- **audit-trail-kafka** → Kafka Operator deployment or external Kafka service

### Multi-Buildpack Architecture
**Current CF Setup:**
```yaml
buildpacks:
  - java_buildpack    # Primary Spring Boot application
  - python_buildpack  # ML model inference components
```

**Kubernetes Replacement Strategy:**
- **Multi-stage Dockerfile**: Build Java application and Python ML components separately
- **Init Containers**: Use Python init container to prepare ML models
- **Sidecar Pattern**: Deploy Python ML service as sidecar container
- **Shared Volumes**: Mount ML models via shared persistent volume

### Service Discovery & Routing
**Current CF Features:**
- **Routes**: credit-scoring.internal.banking.com, credit-api-v3.banking.com
- **Health Checks**: HTTP endpoint /actuator/health/detailed with 20s timeout
- **Load Balancing**: Automatic across 4 CF instances

**Kubernetes Replacement:**
- **OpenShift Routes/Ingress**: Replace CF routes with K8s ingress controllers
- **Service Discovery**: Kubernetes DNS-based service discovery
- **Load Balancing**: Kubernetes Service with ClusterIP for internal, LoadBalancer for external
- **Health Probes**: liveness/readiness probes replacing CF health checks
