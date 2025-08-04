#!/bin/bash


set -e

echo "🔍 Validating Kubernetes manifests against k8s standards..."

K8S_DIR="k8s"
FAILED_CHECKS=0

echo "📊 Rule 01: Checking resource requests & limits..."
if ! grep -q "resources:" "$K8S_DIR/deployment.yaml"; then
    echo "❌ FAIL: No resources section found"
    FAILED_CHECKS=$((FAILED_CHECKS + 1))
elif ! grep -A 10 "resources:" "$K8S_DIR/deployment.yaml" | grep -q "requests:" || \
     ! grep -A 10 "resources:" "$K8S_DIR/deployment.yaml" | grep -q "limits:"; then
    echo "❌ FAIL: Missing resource requests or limits"
    FAILED_CHECKS=$((FAILED_CHECKS + 1))
else
    echo "✅ PASS: Resource requests & limits found"
fi

echo "🔒 Rule 02: Checking pod security context..."
SECURITY_CHECKS=0

if grep -q "runAsNonRoot: true" "$K8S_DIR/deployment.yaml"; then
    echo "✅ PASS: runAsNonRoot: true"
else
    echo "❌ FAIL: runAsNonRoot not set to true"
    FAILED_CHECKS=$((FAILED_CHECKS + 1))
    SECURITY_CHECKS=$((SECURITY_CHECKS + 1))
fi

if grep -q "type: RuntimeDefault" "$K8S_DIR/deployment.yaml"; then
    echo "✅ PASS: seccompProfile: RuntimeDefault"
else
    echo "❌ FAIL: seccompProfile not set to RuntimeDefault"
    FAILED_CHECKS=$((FAILED_CHECKS + 1))
    SECURITY_CHECKS=$((SECURITY_CHECKS + 1))
fi

if grep -q "readOnlyRootFilesystem: true" "$K8S_DIR/deployment.yaml"; then
    echo "✅ PASS: readOnlyRootFilesystem: true"
else
    echo "❌ FAIL: readOnlyRootFilesystem not set to true"
    FAILED_CHECKS=$((FAILED_CHECKS + 1))
    SECURITY_CHECKS=$((SECURITY_CHECKS + 1))
fi

if grep -q 'drop: \["ALL"\]' "$K8S_DIR/deployment.yaml"; then
    echo "✅ PASS: capabilities drop: [\"ALL\"]"
else
    echo "❌ FAIL: capabilities not dropped"
    FAILED_CHECKS=$((FAILED_CHECKS + 1))
    SECURITY_CHECKS=$((SECURITY_CHECKS + 1))
fi

echo "🏷️  Rule 03: Checking image provenance..."
if grep -q ":latest" "$K8S_DIR/deployment.yaml"; then
    echo "❌ FAIL: Found :latest tag (forbidden)"
    FAILED_CHECKS=$((FAILED_CHECKS + 1))
elif grep -q "@sha256:" "$K8S_DIR/deployment.yaml"; then
    echo "✅ PASS: Image uses digest pinning"
elif grep -q "registry.bank.internal" "$K8S_DIR/deployment.yaml"; then
    echo "✅ PASS: Image from approved internal registry"
else
    echo "❌ FAIL: Image not from approved registry or not pinned"
    FAILED_CHECKS=$((FAILED_CHECKS + 1))
fi

echo "🏷️  Rule 04: Checking mandatory labels..."
REQUIRED_LABELS=("app.kubernetes.io/name" "app.kubernetes.io/version" "app.kubernetes.io/part-of" "environment" "managed-by")

for label in "${REQUIRED_LABELS[@]}"; do
    if grep -q "$label:" "$K8S_DIR/deployment.yaml" && \
       grep -q "$label:" "$K8S_DIR/service.yaml" && \
       grep -q "$label:" "$K8S_DIR/configmap.yaml"; then
        echo "✅ PASS: Label $label found in all resources"
    else
        echo "❌ FAIL: Label $label missing from one or more resources"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
    fi
done

echo ""
echo "📋 Validation Summary:"
if [ $FAILED_CHECKS -eq 0 ]; then
    echo "🎉 All k8s standards checks PASSED!"
    echo "✅ Ready for production deployment"
    exit 0
else
    echo "❌ $FAILED_CHECKS standards violations found"
    echo "🔧 Please fix the issues above before deployment"
    exit 1
fi
