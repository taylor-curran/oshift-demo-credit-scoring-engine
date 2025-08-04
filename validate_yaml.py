#!/usr/bin/env python3
import os
import sys

def basic_yaml_check(filepath):
    """Basic YAML structure validation without requiring yaml module"""
    try:
        with open(filepath, 'r') as f:
            content = f.read().strip()
        
        if not content:
            return False, "File is empty"
        
        if not (content.startswith('apiVersion:') or content.startswith('---')):
            return False, "Missing apiVersion at start"
        
        required_fields = ['apiVersion:', 'kind:', 'metadata:']
        for field in required_fields:
            if field not in content:
                return False, f"Missing required field: {field}"
        
        return True, "Basic structure looks good"
    
    except Exception as e:
        return False, f"Error reading file: {e}"

if __name__ == "__main__":
    yaml_files = ['k8s/deployment.yaml', 'k8s/service.yaml', 'k8s/configmap.yaml']
    
    all_valid = True
    for yaml_file in yaml_files:
        if os.path.exists(yaml_file):
            valid, message = basic_yaml_check(yaml_file)
            print(f"{yaml_file}: {message}")
            if not valid:
                all_valid = False
        else:
            print(f"{yaml_file}: File not found")
            all_valid = False
    
    if all_valid:
        print("All YAML files passed basic validation")
        sys.exit(0)
    else:
        print("Some YAML files failed validation")
        sys.exit(1)
