#!/usr/bin/env python3
import yaml
import sys
import os

def validate_yaml_files(directory):
    yaml_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                yaml_files.append(os.path.join(root, file))

    all_valid = True
    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r') as f:
                yaml.safe_load(f)
            print(f'✓ {yaml_file} - Valid YAML')
        except yaml.YAMLError as e:
            print(f'✗ {yaml_file} - Invalid YAML: {e}')
            all_valid = False
        except Exception as e:
            print(f'✗ {yaml_file} - Error: {e}')
            all_valid = False

    if all_valid:
        print('All YAML files are syntactically valid!')
        return True
    else:
        print('Some YAML files have syntax errors!')
        return False

if __name__ == "__main__":
    directory = sys.argv[1] if len(sys.argv) > 1 else 'k8s/'
    success = validate_yaml_files(directory)
    sys.exit(0 if success else 1)
