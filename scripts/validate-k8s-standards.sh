#!/bin/bash


set +e

echo "🔍 K8s Standards Compliance Validation"
echo "======================================"

K8S_DIR="k8s"
DEPLOYMENT_FILE="$K8S_DIR/deployment.yaml"

if [ ! -d "$K8S_DIR" ]; then
    echo "❌ k8s directory not found"
    exit 1
fi

if [ ! -f "$DEPLOYMENT_FILE" ]; then
    echo "❌ deployment.yaml not found in k8s directory"
    exit 1
fi

echo ""
echo "📋 Rule 01: Resource Requests & Limits"
echo "--------------------------------------"

if grep -q "requests:" "$DEPLOYMENT_FILE" && grep -q "limits:" "$DEPLOYMENT_FILE"; then
    echo "✅ Resource requests and limits are configured"
    
    echo "   CPU Requests: $(grep -A1 "requests:" "$DEPLOYMENT_FILE" | grep "cpu:" | awk '{print $2}' | tr -d '"')"
    echo "   Memory Requests: $(grep -A2 "requests:" "$DEPLOYMENT_FILE" | grep "memory:" | awk '{print $2}' | tr -d '"')"
    echo "   CPU Limits: $(grep -A1 "limits:" "$DEPLOYMENT_FILE" | grep "cpu:" | awk '{print $2}' | tr -d '"')"
    echo "   Memory Limits: $(grep -A2 "limits:" "$DEPLOYMENT_FILE" | grep "memory:" | awk '{print $2}' | tr -d '"')"
else
    echo "❌ Missing resource requests or limits"
    exit 1
fi

echo ""
echo "🔒 Rule 02: Pod Security Baseline"
echo "--------------------------------"

security_checks=0

if grep -q "runAsNonRoot: true" "$DEPLOYMENT_FILE"; then
    echo "✅ runAsNonRoot: true configured"
    ((security_checks++))
else
    echo "❌ Missing runAsNonRoot: true"
fi

if grep -q "readOnlyRootFilesystem: true" "$DEPLOYMENT_FILE"; then
    echo "✅ readOnlyRootFilesystem: true configured"
    ((security_checks++))
else
    echo "❌ Missing readOnlyRootFilesystem: true"
fi

if grep -q 'drop: \["ALL"\]' "$DEPLOYMENT_FILE" || grep -q 'drop: \[\"ALL\"\]' "$DEPLOYMENT_FILE"; then
    echo "✅ capabilities drop: [\"ALL\"] configured"
    ((security_checks++))
else
    echo "❌ Missing capabilities drop: [\"ALL\"]"
fi

if grep -q "RuntimeDefault" "$DEPLOYMENT_FILE"; then
    echo "✅ seccompProfile: RuntimeDefault configured"
    ((security_checks++))
else
    echo "❌ Missing seccompProfile: RuntimeDefault"
fi

if [ $security_checks -ne 4 ]; then
    echo "❌ Security baseline not fully implemented ($security_checks/4 checks passed)"
    exit 1
fi

echo ""
echo "🏷️  Rule 03: Image Provenance"
echo "-----------------------------"

if grep -q ":latest" "$K8S_DIR"/*.yaml 2>/dev/null; then
    echo "❌ Found :latest tag in manifests (not allowed)"
    exit 1
else
    echo "✅ No :latest tags found"
fi

if grep -q "@sha256:" "$DEPLOYMENT_FILE"; then
    echo "✅ SHA digest found in image reference"
    image_ref=$(grep "image:" "$DEPLOYMENT_FILE" | awk '{print $2}')
    echo "   Image: $image_ref"
else
    echo "❌ Missing SHA digest in image reference"
    exit 1
fi

echo ""
echo "🏷️  Rule 04: Naming & Label Conventions"
echo "--------------------------------------"

required_labels=("app.kubernetes.io/name" "app.kubernetes.io/version" "app.kubernetes.io/part-of" "environment" "managed-by")
missing_labels=()

for label in "${required_labels[@]}"; do
    if grep -q "$label:" "$DEPLOYMENT_FILE"; then
        echo "✅ $label: $(grep "$label:" "$DEPLOYMENT_FILE" | head -1 | awk '{print $2}' | tr -d '"')"
    else
        echo "❌ Missing required label: $label"
        missing_labels+=("$label")
    fi
done

if [ ${#missing_labels[@]} -ne 0 ]; then
    echo "❌ Missing required labels: ${missing_labels[*]}"
    exit 1
fi

echo ""
echo "🎉 K8s Standards Compliance Summary"
echo "=================================="
echo "✅ Rule 01: Resource Requests & Limits - PASSED"
echo "✅ Rule 02: Pod Security Baseline - PASSED"
echo "✅ Rule 03: Image Provenance - PASSED"
echo "✅ Rule 04: Naming & Labels - PASSED"
echo ""
echo "🏆 All k8s standards compliance checks passed successfully!"
echo ""
echo "📊 Additional Checks:"

if grep -q "livenessProbe:" "$DEPLOYMENT_FILE" && grep -q "readinessProbe:" "$DEPLOYMENT_FILE"; then
    echo "✅ Health probes configured (liveness & readiness)"
else
    echo "⚠️  Health probes not fully configured"
fi

if grep -q "prometheus.io/scrape" "$K8S_DIR"/*.yaml 2>/dev/null; then
    echo "✅ Prometheus observability annotations found"
else
    echo "⚠️  Prometheus annotations not found"
fi

echo ""
echo "✨ Validation complete! Your k8s manifests are standards compliant."
