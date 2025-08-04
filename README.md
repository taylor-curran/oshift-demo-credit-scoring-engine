# Credit Scoring Engine

## Artifact Design Thinking

**Platform**: Kubernetes with Helm | **Complexity**: High

Sophisticated credit risk assessment system demonstrating enterprise ML/regulatory patterns with full k8s standards compliance:

- **Kubernetes-native deployment** - Complete migration from Cloud Foundry to k8s
- **Multi-buildpack setup** - Java + Python for hybrid ML/enterprise architecture
- **Credit bureau integrations** - Experian, Equifax, TransUnion APIs
- **Multiple scoring models** - FICO, VantageScore, proprietary ML models
- **Regulatory compliance** - FCRA, ECOA with adverse action notifications
- **K8s standards compliance** - Security contexts, resource limits, image provenance, proper labeling
- **A/B testing framework** - model performance comparison

### Key Features
- Integration with 3 major credit bureaus
- Multiple scoring algorithms and regulatory compliance automation
- ML model management with A/B testing and decision engine logic
- Full Kubernetes standards compliance (Rules 01-04)
- Multi-environment Helm chart deployment (dev/test/prod)

### K8s Standards Compliance

This application implements all enterprise Kubernetes standards:

- **Rule 01 - Resource Limits**: CPU/memory requests and limits enforced
- **Rule 02 - Security Context**: Pod Security Baseline with runAsNonRoot, seccomp, readOnlyRootFilesystem
- **Rule 03 - Image Provenance**: Pinned images with SHA digests from trusted registry
- **Rule 04 - Naming & Labels**: Proper app.kubernetes.io labels and naming conventions

## Quick Start

### Prerequisites
- Java 17, Maven 3.6+
- Kubernetes cluster (for deployment)
- Helm 3.x (for k8s deployment)

### Local Development
```bash
# Install dependencies
mvn clean install

# Run tests
mvn test

# Run locally (uses H2 in-memory DB)
mvn spring-boot:run
```

### Kubernetes Deployment

#### Option 1: Direct kubectl deployment
```bash
# Deploy to Kubernetes
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n credit-scoring -l app.kubernetes.io/name=credit-scoring-engine

# Port forward for testing
kubectl port-forward -n credit-scoring svc/pe-eng-credit-scoring-engine-prod 8080:80
```

#### Option 2: Helm deployment (recommended)
```bash
# Install for production
helm install credit-scoring-prod ./helm

# Install for development
helm install credit-scoring-dev ./helm -f helm/values-dev.yaml

# Install for test
helm install credit-scoring-test ./helm -f helm/values-test.yaml

# Upgrade deployment
helm upgrade credit-scoring-prod ./helm
```

### Health Checks
```bash
# Check application health
curl http://localhost:8080/actuator/health/detailed

# Check readiness
curl http://localhost:8080/actuator/health/readiness

# Check liveness
curl http://localhost:8080/actuator/health/liveness

# View Prometheus metrics
curl http://localhost:8080/actuator/prometheus
```

### API Testing
```bash
# Test credit scoring endpoint
curl -X POST http://localhost:8080/api/v1/credit/score \
  -H "Content-Type: application/json" \
  -d '{
    "applicantId": "12345",
    "paymentHistory": 0.95,
    "creditUtilization": 0.25,
    "creditHistoryMonths": 120,
    "debtToIncomeRatio": 0.35,
    "consentProvided": true
  }'
```

## Architecture

### Cloud Foundry → Kubernetes Migration

This application has been migrated from Cloud Foundry to Kubernetes with the following changes:

| Component | Cloud Foundry | Kubernetes |
|-----------|---------------|------------|
| **Deployment** | `manifest.yml` | `k8s/deployment.yaml` + Helm chart |
| **Memory** | 3072M | 2Gi (with 1536Mi requests) |
| **Instances** | 4 | 4 replicas |
| **Health Checks** | CF health-check | Liveness/readiness probes |
| **Routing** | CF routes | Ingress with nginx |
| **Services** | CF services | External service connections |
| **Security** | CF security groups | Pod security contexts |

### Environment Configuration

- **Development**: Single replica, H2 database, reduced resources
- **Test**: 2 replicas, PostgreSQL, moderate resources  
- **Production**: 4 replicas, full PostgreSQL/Redis stack, full resources

## Legacy Cloud Foundry Deployment

For legacy Cloud Foundry deployments (deprecated):
```bash
cf push
```
