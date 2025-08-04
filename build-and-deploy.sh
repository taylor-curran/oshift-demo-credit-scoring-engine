#!/bin/bash
set -e


echo "🏗️  Building Credit Scoring Engine..."

mvn clean package -DskipTests

IMAGE_TAG="registry.bank.internal/credit-scoring-engine:3.1.0"
echo "🐳 Building Docker image: $IMAGE_TAG"

docker build -t "$IMAGE_TAG" .

echo "📝 Image built successfully. Remember to:"
echo "   1. Push to registry: docker push $IMAGE_TAG"
echo "   2. Update deployment.yaml with actual SHA digest"
echo "   3. Sign image with Cosign for production"

echo "🚀 Ready for Kubernetes deployment!"
echo "   Deploy with: helm install credit-scoring-engine ./helm/credit-scoring-engine --namespace retail-banking --create-namespace"
