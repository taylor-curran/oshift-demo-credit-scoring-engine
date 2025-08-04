#!/usr/bin/env python3
"""
K8s Standards Validation Script
Validates Kubernetes manifests against the four enterprise k8s standards
"""

import yaml
import os
import sys
from pathlib import Path

def load_yaml_files(k8s_dir):
    """Load all YAML files from k8s directory"""
    yaml_files = {}
    for file_path in Path(k8s_dir).glob("*.yaml"):
        with open(file_path, 'r') as f:
            try:
                docs = list(yaml.safe_load_all(f))
                yaml_files[file_path.name] = docs
            except yaml.YAMLError as e:
                print(f"ERROR: Invalid YAML in {file_path}: {e}")
                return None
    return yaml_files

def validate_rule_01_resources(manifests):
    """Rule 01: Resource Requests & Limits"""
    issues = []
    
    for filename, docs in manifests.items():
        for doc in docs:
            if doc and doc.get('kind') == 'Deployment':
                containers = doc.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])
                for i, container in enumerate(containers):
                    resources = container.get('resources', {})
                    requests = resources.get('requests', {})
                    limits = resources.get('limits', {})
                    
                    if not requests or not limits:
                        issues.append(f"{filename}: Container {i} missing resource requests/limits")
                        continue
                    
                    if 'cpu' not in requests or 'cpu' not in limits:
                        issues.append(f"{filename}: Container {i} missing CPU requests/limits")
                    
                    if 'memory' not in requests or 'memory' not in limits:
                        issues.append(f"{filename}: Container {i} missing memory requests/limits")
    
    return issues

def validate_rule_02_security(manifests):
    """Rule 02: Pod Security Baseline"""
    issues = []
    
    for filename, docs in manifests.items():
        for doc in docs:
            if doc and doc.get('kind') == 'Deployment':
                pod_spec = doc.get('spec', {}).get('template', {}).get('spec', {})
                pod_security = pod_spec.get('securityContext', {})
                
                if not pod_security.get('runAsNonRoot'):
                    issues.append(f"{filename}: Missing runAsNonRoot: true in pod securityContext")
                
                if pod_security.get('seccompProfile', {}).get('type') != 'RuntimeDefault':
                    issues.append(f"{filename}: Missing seccompProfile.type: RuntimeDefault in pod securityContext")
                
                containers = pod_spec.get('containers', [])
                for i, container in enumerate(containers):
                    container_security = container.get('securityContext', {})
                    
                    if not container_security.get('runAsNonRoot'):
                        issues.append(f"{filename}: Container {i} missing runAsNonRoot: true")
                    
                    if not container_security.get('readOnlyRootFilesystem'):
                        issues.append(f"{filename}: Container {i} missing readOnlyRootFilesystem: true")
                    
                    capabilities = container_security.get('capabilities', {})
                    if capabilities.get('drop') != ['ALL']:
                        issues.append(f"{filename}: Container {i} missing capabilities.drop: ['ALL']")
                    
                    if container_security.get('seccompProfile', {}).get('type') != 'RuntimeDefault':
                        issues.append(f"{filename}: Container {i} missing seccompProfile.type: RuntimeDefault")
    
    return issues

def validate_rule_03_images(manifests):
    """Rule 03: Immutable, Trusted Images"""
    issues = []
    
    for filename, docs in manifests.items():
        for doc in docs:
            if doc and doc.get('kind') == 'Deployment':
                containers = doc.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])
                for i, container in enumerate(containers):
                    image = container.get('image', '')
                    
                    if image.endswith(':latest') or ':latest@' in image:
                        issues.append(f"{filename}: Container {i} uses :latest tag: {image}")
                    
                    approved_registries = ['registry.bank.internal/', 'quay.io/redhat-openshift-approved/']
                    if not any(image.startswith(registry) for registry in approved_registries):
                        issues.append(f"{filename}: Container {i} uses non-approved registry: {image}")
                    
                    if '@sha256:' not in image and not image.endswith(':latest'):
                        print(f"WARNING: {filename}: Container {i} not pinned with digest: {image}")
    
    return issues

def validate_rule_04_labels(manifests):
    """Rule 04: Naming & Label Conventions"""
    issues = []
    required_labels = [
        'app.kubernetes.io/name',
        'app.kubernetes.io/version', 
        'app.kubernetes.io/part-of',
        'environment',
        'managed-by'
    ]
    
    for filename, docs in manifests.items():
        for doc in docs:
            if doc and doc.get('kind') in ['Deployment', 'Service', 'ConfigMap', 'Secret', 'Ingress', 'Namespace']:
                labels = doc.get('metadata', {}).get('labels', {})
                
                for required_label in required_labels:
                    if required_label not in labels:
                        issues.append(f"{filename}: Missing required label: {required_label}")
                
                name = doc.get('metadata', {}).get('name', '')
                if doc.get('kind') != 'Namespace' and not name.startswith('pe-eng-'):
                    issues.append(f"{filename}: Name doesn't follow convention (should start with 'pe-eng-'): {name}")
    
    return issues

def validate_rule_05_observability(manifests):
    """Rule 05: Logging & Observability Hooks"""
    issues = []
    
    for filename, docs in manifests.items():
        for doc in docs:
            if doc and doc.get('kind') == 'Deployment':
                pod_annotations = doc.get('spec', {}).get('template', {}).get('metadata', {}).get('annotations', {})
                
                if pod_annotations.get('prometheus.io/scrape') != 'true':
                    issues.append(f"{filename}: Missing prometheus.io/scrape: 'true' annotation")
                
                if pod_annotations.get('prometheus.io/port') != '8080':
                    issues.append(f"{filename}: Missing or incorrect prometheus.io/port: '8080' annotation")
                
                if not pod_annotations.get('prometheus.io/path'):
                    issues.append(f"{filename}: Missing prometheus.io/path annotation")
            
            elif doc and doc.get('kind') == 'Service':
                service_annotations = doc.get('metadata', {}).get('annotations', {})
                
                if service_annotations.get('prometheus.io/scrape') != 'true':
                    issues.append(f"{filename}: Service missing prometheus.io/scrape: 'true' annotation")
                
                if service_annotations.get('prometheus.io/port') != '8080':
                    issues.append(f"{filename}: Service missing or incorrect prometheus.io/port: '8080' annotation")
    
    return issues

def validate_rule_06_health_probes(manifests):
    """Rule 06: Liveness & Readiness Probes"""
    issues = []
    
    for filename, docs in manifests.items():
        for doc in docs:
            if doc and doc.get('kind') == 'Deployment':
                containers = doc.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])
                for i, container in enumerate(containers):
                    liveness_probe = container.get('livenessProbe', {})
                    readiness_probe = container.get('readinessProbe', {})
                    
                    if not liveness_probe:
                        issues.append(f"{filename}: Container {i} missing livenessProbe")
                    else:
                        liveness_path = liveness_probe.get('httpGet', {}).get('path', '')
                        if '/actuator/health/liveness' not in liveness_path:
                            issues.append(f"{filename}: Container {i} liveness probe should use /actuator/health/liveness")
                        
                        if liveness_probe.get('initialDelaySeconds', 0) < 30:
                            issues.append(f"{filename}: Container {i} liveness probe initialDelaySeconds should be >= 30s")
                    
                    if not readiness_probe:
                        issues.append(f"{filename}: Container {i} missing readinessProbe")
                    else:
                        readiness_path = readiness_probe.get('httpGet', {}).get('path', '')
                        if '/actuator/health/readiness' not in readiness_path:
                            issues.append(f"{filename}: Container {i} readiness probe should use /actuator/health/readiness")
                        
                        if readiness_probe.get('initialDelaySeconds', 0) < 10:
                            issues.append(f"{filename}: Container {i} readiness probe initialDelaySeconds should be >= 10s")
    
    return issues

def main():
    k8s_dir = "k8s"
    if not os.path.exists(k8s_dir):
        print(f"ERROR: {k8s_dir} directory not found")
        sys.exit(1)
    
    print("🔍 Loading Kubernetes manifests...")
    manifests = load_yaml_files(k8s_dir)
    if manifests is None:
        sys.exit(1)
    
    print(f"📋 Found {len(manifests)} manifest files")
    
    all_issues = []
    
    print("\n📏 Rule 01: Resource Requests & Limits")
    rule_01_issues = validate_rule_01_resources(manifests)
    all_issues.extend(rule_01_issues)
    if rule_01_issues:
        for issue in rule_01_issues:
            print(f"  ❌ {issue}")
    else:
        print("  ✅ All containers have proper resource requests and limits")
    
    print("\n🔒 Rule 02: Pod Security Baseline")
    rule_02_issues = validate_rule_02_security(manifests)
    all_issues.extend(rule_02_issues)
    if rule_02_issues:
        for issue in rule_02_issues:
            print(f"  ❌ {issue}")
    else:
        print("  ✅ All pods follow security baseline requirements")
    
    print("\n🖼️  Rule 03: Immutable, Trusted Images")
    rule_03_issues = validate_rule_03_images(manifests)
    all_issues.extend(rule_03_issues)
    if rule_03_issues:
        for issue in rule_03_issues:
            print(f"  ❌ {issue}")
    else:
        print("  ✅ All images are from trusted registries and properly tagged")
    
    print("\n🏷️  Rule 04: Naming & Label Conventions")
    rule_04_issues = validate_rule_04_labels(manifests)
    all_issues.extend(rule_04_issues)
    if rule_04_issues:
        for issue in rule_04_issues:
            print(f"  ❌ {issue}")
    else:
        print("  ✅ All resources follow naming and labeling conventions")
    
    print("\n📊 Rule 05: Logging & Observability Hooks")
    rule_05_issues = validate_rule_05_observability(manifests)
    all_issues.extend(rule_05_issues)
    if rule_05_issues:
        for issue in rule_05_issues:
            print(f"  ❌ {issue}")
    else:
        print("  ✅ All services have proper Prometheus annotations for observability")
    
    print("\n🩺 Rule 06: Liveness & Readiness Probes")
    rule_06_issues = validate_rule_06_health_probes(manifests)
    all_issues.extend(rule_06_issues)
    if rule_06_issues:
        for issue in rule_06_issues:
            print(f"  ❌ {issue}")
    else:
        print("  ✅ All containers have proper health probes configured")
    
    print(f"\n📊 Summary: {len(all_issues)} issues found")
    
    if all_issues:
        print("\n🔧 Issues to fix:")
        for issue in all_issues:
            print(f"  • {issue}")
        sys.exit(1)
    else:
        print("\n🎉 All k8s standards compliance checks passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()
