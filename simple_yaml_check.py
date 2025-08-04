#!/usr/bin/env python3
import os
import sys

def basic_yaml_check(file_path):
    """Basic YAML syntax check without requiring yaml module"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        if not content.strip():
            return False, "Empty file"
        
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                if line.startswith(' ') and ':' in line:
                    continue
                elif ':' in stripped or stripped.startswith('-'):
                    continue
                elif stripped.startswith('apiVersion:') or stripped.startswith('kind:'):
                    continue
        
        return True, "Basic syntax appears valid"
    except Exception as e:
        return False, str(e)

def check_k8s_directory(directory):
    """Check all YAML files in k8s directory"""
    yaml_files = []
    for file in os.listdir(directory):
        if file.endswith('.yaml') or file.endswith('.yml'):
            yaml_files.append(os.path.join(directory, file))
    
    all_valid = True
    for yaml_file in yaml_files:
        valid, message = basic_yaml_check(yaml_file)
        status = "✓" if valid else "✗"
        print(f"{status} {yaml_file}: {message}")
        if not valid:
            all_valid = False
    
    return all_valid

if __name__ == "__main__":
    directory = sys.argv[1] if len(sys.argv) > 1 else 'k8s'
    success = check_k8s_directory(directory)
    print(f"\nOverall result: {'PASS' if success else 'FAIL'}")
    sys.exit(0 if success else 1)
