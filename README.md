# Credit Scoring Engine

## Artifact Design Thinking

**Platform**: Kubernetes/OpenShift | **Complexity**: High

Sophisticated credit risk assessment system demonstrating enterprise ML/regulatory patterns with full k8s standards compliance:

- **Multi-buildpack setup** - Java + Python for hybrid ML/enterprise architecture
- **Credit bureau integrations** - Experian, Equifax, TransUnion APIs
- **Multiple scoring models** - FICO, VantageScore, proprietary ML models
- **Regulatory compliance** - FCRA, ECOA with adverse action notifications
- **High-memory allocation** - 3GB for complex ML model inference
- **A/B testing framework** - model performance comparison
- **K8s Standards Compliant** - Follows Rules 01-06 for security, observability, and operational excellence

### Key Features
- Integration with 3 major credit bureaus
- Multiple scoring algorithms and regulatory compliance automation
- ML model management with A/B testing and decision engine logic
- Full Kubernetes deployment with security baselines and observability

## Quick Start

### Prerequisites
- Java 17, Maven 3.6+
- Kubernetes cluster (for k8s deployment)

### Run Locally
```bash
# Install dependencies
mvn clean install

# Run tests
mvn test

# Run locally (uses H2 in-memory DB)
mvn spring-boot:run
```

### Deploy to Kubernetes
```bash
# Apply Kubernetes manifests
kubectl apply -k k8s/

# Or using kustomize
kustomize build k8s/ | kubectl apply -f -
```

### Deploy to Cloud Foundry (Legacy)
```bash
cf push
```

## Kubernetes Standards Compliance

This application follows the k8s standards (Rules 01-04):

- **Rule 01**: Resource requests/limits properly configured ✅
- **Rule 02**: Pod security baseline with non-root user, seccomp, read-only filesystem ✅
- **Rule 03**: Pinned image tags from approved registry ✅
- **Rule 04**: Proper naming conventions and mandatory labels ✅

**Audit Status**: FULLY COMPLIANT - See [K8S_STANDARDS_AUDIT.md](K8S_STANDARDS_AUDIT.md) for detailed audit report.

See [k8s/README.md](k8s/README.md) for deployment instructions.
