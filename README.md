# Credit Scoring Engine

## Artifact Design Thinking

**Platform**: Traditional Cloud Foundry + Kubernetes | **Complexity**: High

Sophisticated credit risk assessment system demonstrating enterprise ML/regulatory patterns:

- **Multi-buildpack setup** - Java + Python for hybrid ML/enterprise architecture
- **Credit bureau integrations** - Experian, Equifax, TransUnion APIs
- **Multiple scoring models** - FICO, VantageScore, proprietary ML models
- **Regulatory compliance** - FCRA, ECOA with adverse action notifications
- **High-memory allocation** - 3GB for complex ML model inference
- **A/B testing framework** - model performance comparison

### Key Features
- Integration with 3 major credit bureaus
- Multiple scoring algorithms and regulatory compliance automation
- ML model management with A/B testing and decision engine logic

## K8s Standards Compliance ✅

This application includes **fully compliant** Kubernetes manifests that meet all enterprise k8s standards:

- **Resource Management**: Proper CPU/memory requests and limits with 60% ratios for HPA headroom
- **Security**: Non-root execution, read-only filesystem, dropped capabilities, seccomp profiles
- **Image Provenance**: Pinned image tags with SHA256 digests from approved registries
- **Observability**: Prometheus metrics, JSON logging, comprehensive health probes
- **Labeling**: Standard Kubernetes labels for discoverability and cost tracking

**Audit Status**: ✅ FULLY COMPLIANT (see `K8S-STANDARDS-AUDIT.md` for detailed verification)

### Kubernetes Deployment
```bash
# Apply all Kubernetes manifests
kubectl apply -k k8s/

# Or apply individually
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/ingress.yaml
```

## Quick Start

### Prerequisites
- Java 17, Maven 3.6+

### Run
```bash
# Install dependencies
mvn clean install

# Run tests
mvn test

# Run locally (uses H2 in-memory DB)
mvn spring-boot:run
```

### Deploy

#### Cloud Foundry (Legacy)
```bash
cf push
```

#### Kubernetes (Recommended)
```bash
kubectl apply -k k8s/
```
