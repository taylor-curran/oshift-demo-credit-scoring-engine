# Cloud Foundry to OpenShift Migration Analysis

## Phase 1: Investigation Complete

### 1. Artifact Purposes
- **manifest.yml**: Defines 4 instances, 3GB memory, multi-buildpack (Java + Python)
- **pom.xml**: Maven build with Spring Boot 2.7.8, Java 17
- **JAR artifact**: Target is `credit-scoring-engine-3.1.0.jar`

### 2. Dependencies & Integrations
- **Bound Services (7 total)**:
  - credit-postgres-primary/replica
  - credit-redis-cluster  
  - model-storage-s3
  - credit-bureau-proxy
  - encryption-service
  - audit-trail-kafka

- **External APIs**:
  - Experian, Equifax, TransUnion credit bureaus
  - The Work Number (income verification)
  - Plaid (bank statement analysis)

### 3. Resource Requirements
- **CF Config**: 4 instances × 3GB memory, 5GB disk
- **JVM**: 2560m heap, G1GC, String deduplication
- **Kubernetes Target**: 4 replicas, appropriate resource limits

### 4. Build Process
- Maven-based Spring Boot application
- Current: `cf push` with JAR artifact
- Target: Docker build + `oc apply`

### 5. Security & Compliance
- FCRA and ECOA compliance modes
- Health check endpoint: `/actuator/health/detailed`
- Consent validation required

### 6. Platform-Specific Features
- Multi-buildpack (Java + Python) - needs custom Dockerfile
- VCAP_SERVICES → ConfigMaps/Secrets conversion
- CF routes → OpenShift Routes/Ingress

## Migration Todo List

### Phase 2: Scaffold Conversion
1. **Create Dockerfile** - Replace CF buildpacks with container build
2. **Generate Kubernetes Manifests**:
   - Deployment with resource limits & security context
   - Service (ClusterIP)
   - ConfigMap for environment variables
   - Secret for sensitive data
   - Route/Ingress for external access

### Phase 3: Standards Compliance
3. **Apply Resource Limits** (Rule 01)
4. **Apply Security Context** (Rule 02) 
5. **Apply Image Provenance** (Rule 03)
6. **Apply Naming & Labels** (Rule 04)

### Phase 4: Build & Deploy
7. **Build and load image locally**
8. **Deploy to local OpenShift**
9. **Verify deployment quality**

### Phase 5: Finalize
10. **Create PR with migration artifacts**
11. **Wait for CI checks**
12. **Report to user**
