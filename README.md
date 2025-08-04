# Credit Scoring Engine

## Artifact Design Thinking

**Platform**: Traditional Cloud Foundry | **Complexity**: High

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

#### Cloud Foundry
```bash
cf push
```

#### Kubernetes
```bash
# Build and push container image
docker build -t registry.bank.internal/credit-scoring-engine:3.1.0 .
docker push registry.bank.internal/credit-scoring-engine:3.1.0

# Deploy using Helm (recommended)
helm install credit-scoring-engine ./helm/credit-scoring-engine \
  --namespace retail-banking \
  --create-namespace

# Or deploy using kubectl
kubectl apply -f k8s/
```

## Kubernetes Standards Compliance

This application is fully compliant with k8s-standards-library rules:

- **Rule 01**: Resource requests/limits configured
- **Rule 02**: Pod security baseline with non-root user, seccomp, read-only filesystem
- **Rule 03**: Pinned image tags from approved registry
- **Rule 04**: Proper naming conventions and mandatory labels
- **Rule 05**: JSON logging and Prometheus metrics on port 8080
- **Rule 06**: Health probes for liveness and readiness

See [k8s/README.md](k8s/README.md) for detailed deployment instructions.
