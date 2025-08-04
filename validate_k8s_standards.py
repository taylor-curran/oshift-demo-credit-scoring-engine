#!/usr/bin/env python3
"""
K8s Standards Compliance Validator
Validates YAML manifests against the 6 k8s standards rules.
"""

import yaml
import sys
import re
from pathlib import Path

def load_yaml_files(k8s_dir):
    """Load all YAML files from k8s directory."""
    manifests = {}
    for yaml_file in Path(k8s_dir).glob("*.yaml"):
        if yaml_file.name == "README.md":
            continue
        with open(yaml_file, 'r') as f:
            try:
                content = yaml.safe_load(f)
                manifests[yaml_file.name] = content
            except yaml.YAMLError as e:
                print(f"❌ YAML syntax error in {yaml_file.name}: {e}")
                return None
    return manifests

def validate_rule_01_resources(manifests):
    """Rule 01: Enforce Resource Requests & Limits"""
    print("🔍 Rule 01 - Resource Limits")
    
    for filename, manifest in manifests.items():
        if manifest.get('kind') == 'Deployment':
            containers = manifest.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])
            for container in containers:
                resources = container.get('resources', {})
                requests = resources.get('requests', {})
                limits = resources.get('limits', {})
                
                if not requests.get('cpu'):
                    print(f"❌ {filename}: Missing CPU requests")
                    return False
                if not requests.get('memory'):
                    print(f"❌ {filename}: Missing memory requests")
                    return False
                if not limits.get('cpu'):
                    print(f"❌ {filename}: Missing CPU limits")
                    return False
                if not limits.get('memory'):
                    print(f"❌ {filename}: Missing memory limits")
                    return False
                    
                print(f"✅ {filename}: Resource limits properly configured")
    return True

def validate_rule_02_security(manifests):
    """Rule 02: Pod Security Baseline"""
    print("🔍 Rule 02 - Security Context")
    
    for filename, manifest in manifests.items():
        if manifest.get('kind') == 'Deployment':
            pod_spec = manifest.get('spec', {}).get('template', {}).get('spec', {})
            pod_security = pod_spec.get('securityContext', {})
            
            if not pod_security.get('runAsNonRoot'):
                print(f"❌ {filename}: Missing pod runAsNonRoot")
                return False
            if pod_security.get('seccompProfile', {}).get('type') != 'RuntimeDefault':
                print(f"❌ {filename}: Missing pod seccompProfile")
                return False
                
            containers = pod_spec.get('containers', [])
            for container in containers:
                sec_ctx = container.get('securityContext', {})
                if not sec_ctx.get('runAsNonRoot'):
                    print(f"❌ {filename}: Missing container runAsNonRoot")
                    return False
                if not sec_ctx.get('readOnlyRootFilesystem'):
                    print(f"❌ {filename}: Missing readOnlyRootFilesystem")
                    return False
                if 'ALL' not in sec_ctx.get('capabilities', {}).get('drop', []):
                    print(f"❌ {filename}: Missing capabilities drop ALL")
                    return False
                if sec_ctx.get('allowPrivilegeEscalation') is not False:
                    print(f"❌ {filename}: allowPrivilegeEscalation should be false")
                    return False
                    
            print(f"✅ {filename}: Security context properly configured")
    return True

def validate_rule_03_images(manifests):
    """Rule 03: Immutable, Trusted Images"""
    print("🔍 Rule 03 - Image Provenance")
    
    for filename, manifest in manifests.items():
        if manifest.get('kind') == 'Deployment':
            containers = manifest.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])
            for container in containers:
                image = container.get('image', '')
                
                if image.endswith(':latest'):
                    print(f"❌ {filename}: Image uses :latest tag")
                    return False
                    
                if not (image.startswith('registry.bank.internal/') or 
                       image.startswith('quay.io/redhat-openshift-approved/')):
                    print(f"❌ {filename}: Image not from approved registry")
                    return False
                    
                if '@sha256:' not in image:
                    print(f"❌ {filename}: Image not pinned with digest")
                    return False
                    
                print(f"✅ {filename}: Image provenance compliant")
    return True

def validate_rule_04_naming(manifests):
    """Rule 04: Naming & Label Conventions"""
    print("🔍 Rule 04 - Naming & Labels")
    
    required_labels = [
        'app.kubernetes.io/name',
        'app.kubernetes.io/version', 
        'app.kubernetes.io/part-of',
        'environment',
        'managed-by'
    ]
    
    for filename, manifest in manifests.items():
        labels = manifest.get('metadata', {}).get('labels', {})
        
        for label in required_labels:
            if label not in labels:
                print(f"❌ {filename}: Missing required label {label}")
                return False
                
        name = manifest.get('metadata', {}).get('name', '')
        if not re.match(r'^[a-z]+-[a-z]+-[a-z-]+-[a-z]+$', name):
            print(f"❌ {filename}: Name doesn't follow team-app-env convention")
            return False
            
        print(f"✅ {filename}: Naming and labels compliant")
    return True

def validate_rule_05_observability(manifests):
    """Rule 05: Logging & Observability"""
    print("🔍 Rule 05 - Logging & Observability")
    
    for filename, manifest in manifests.items():
        if manifest.get('kind') in ['Deployment', 'Service']:
            annotations = manifest.get('metadata', {}).get('annotations', {})
            
            if 'prometheus.io/scrape' not in annotations:
                print(f"❌ {filename}: Missing prometheus.io/scrape annotation")
                return False
            if 'prometheus.io/port' not in annotations:
                print(f"❌ {filename}: Missing prometheus.io/port annotation")
                return False
                
            print(f"✅ {filename}: Observability annotations present")
    return True

def validate_rule_06_health_probes(manifests):
    """Rule 06: Health Probes"""
    print("🔍 Rule 06 - Health Probes")
    
    for filename, manifest in manifests.items():
        if manifest.get('kind') == 'Deployment':
            containers = manifest.get('spec', {}).get('template', {}).get('spec', {}).get('containers', [])
            for container in containers:
                liveness = container.get('livenessProbe')
                if not liveness:
                    print(f"❌ {filename}: Missing liveness probe")
                    return False
                    
                readiness = container.get('readinessProbe')
                if not readiness:
                    print(f"❌ {filename}: Missing readiness probe")
                    return False
                    
                print(f"✅ {filename}: Health probes configured")
    return True

def main():
    """Main validation function."""
    print("🚀 K8s Standards Compliance Validator")
    print("=" * 50)
    
    k8s_dir = "k8s"
    if not Path(k8s_dir).exists():
        print(f"❌ Directory {k8s_dir} not found")
        sys.exit(1)
        
    manifests = load_yaml_files(k8s_dir)
    if manifests is None:
        sys.exit(1)
        
    print(f"📁 Found {len(manifests)} YAML files")
    print()
    
    rules = [
        validate_rule_01_resources,
        validate_rule_02_security, 
        validate_rule_03_images,
        validate_rule_04_naming,
        validate_rule_05_observability,
        validate_rule_06_health_probes
    ]
    
    all_passed = True
    for rule in rules:
        if not rule(manifests):
            all_passed = False
        print()
        
    if all_passed:
        print("🎉 All k8s standards compliance checks PASSED!")
        sys.exit(0)
    else:
        print("💥 Some k8s standards compliance checks FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    main()
