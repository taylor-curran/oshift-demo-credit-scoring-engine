#!/usr/bin/env python3

import yaml
import sys
import os

def validate_yaml_files():
    """Validate YAML syntax of all k8s manifest files"""
    k8s_dir = 'k8s'
    if not os.path.exists(k8s_dir):
        print(f"✗ Directory {k8s_dir} not found")
        return False
        
    yaml_files = [f for f in os.listdir(k8s_dir) if f.endswith('.yaml')]
    
    if not yaml_files:
        print(f"✗ No YAML files found in {k8s_dir}")
        return False
    
    all_valid = True
    for file in yaml_files:
        filepath = os.path.join(k8s_dir, file)
        try:
            with open(filepath, 'r') as f:
                docs = list(yaml.safe_load_all(f))
                print(f'✓ {file}: Valid YAML syntax')
        except yaml.YAMLError as e:
            print(f'✗ {file}: YAML syntax error - {e}')
            all_valid = False
        except Exception as e:
            print(f'✗ {file}: Error - {e}')
            all_valid = False
    
    return all_valid

def check_k8s_standards_compliance():
    """Check compliance with all 4 k8s standards"""
    print("\n=== K8s Standards Compliance Check ===")
    
    try:
        with open('k8s/deployment.yaml', 'r') as f:
            deployment = yaml.safe_load(f)
        with open('k8s/service.yaml', 'r') as f:
            service = yaml.safe_load(f)
        with open('k8s/configmap.yaml', 'r') as f:
            configmap = yaml.safe_load(f)
    except Exception as e:
        print(f"✗ Could not load k8s manifests: {e}")
        return False
    
    issues = []
    
    container = deployment['spec']['template']['spec']['containers'][0]
    resources = container.get('resources', {})
    
    if 'requests' not in resources or 'limits' not in resources:
        issues.append("Rule 01: Missing resource requests or limits")
    else:
        requests = resources['requests']
        limits = resources['limits']
        
        if 'cpu' not in requests or 'cpu' not in limits:
            issues.append("Rule 01: Missing CPU requests or limits")
        
        if 'memory' not in requests or 'memory' not in limits:
            issues.append("Rule 01: Missing memory requests or limits")
    
    container_security = container.get('securityContext', {})
    pod_security = deployment['spec']['template']['spec'].get('securityContext', {})
    
    if not container_security.get('runAsNonRoot'):
        issues.append("Rule 02: Missing runAsNonRoot in container securityContext")
    
    if not container_security.get('readOnlyRootFilesystem'):
        issues.append("Rule 02: Missing readOnlyRootFilesystem")
    
    capabilities = container_security.get('capabilities', {})
    if capabilities.get('drop') != ['ALL']:
        issues.append("Rule 02: Must drop ALL capabilities")
    
    if pod_security.get('seccompProfile', {}).get('type') != 'RuntimeDefault':
        issues.append("Rule 02: Missing RuntimeDefault seccompProfile")
    
    image = container.get('image', '')
    if ':latest' in image:
        issues.append("Rule 03: Using :latest tag is forbidden")
    
    if not image.startswith('registry.bank.internal/') and not image.startswith('quay.io/redhat-openshift-approved/'):
        issues.append("Rule 03: Image not from approved registry")
    
    if '@sha256:' not in image:
        issues.append("Rule 03: Image should be pinned with SHA digest")
    
    required_labels = [
        'app.kubernetes.io/name',
        'app.kubernetes.io/version', 
        'app.kubernetes.io/part-of',
        'environment',
        'managed-by'
    ]
    
    labels = deployment['metadata'].get('labels', {})
    for label in required_labels:
        if label not in labels:
            issues.append(f"Rule 04: Missing required label {label}")
    
    deployment_name = deployment['metadata'].get('name', '')
    if not deployment_name.startswith('banking-team-') or not deployment_name.endswith('-prod'):
        issues.append("Rule 04: Deployment name should follow team-app-env pattern")
    
    if issues:
        print("✗ K8s Standards Compliance Issues Found:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✓ All K8s Standards (Rules 01-04) are compliant!")
        return True

if __name__ == "__main__":
    print("=== K8s Manifest Validation ===")
    yaml_valid = validate_yaml_files()
    
    if yaml_valid:
        standards_compliant = check_k8s_standards_compliance()
        if yaml_valid and standards_compliant:
            print("\n✓ All validations passed!")
            sys.exit(0)
    
    print("\n✗ Validation failed!")
    sys.exit(1)
