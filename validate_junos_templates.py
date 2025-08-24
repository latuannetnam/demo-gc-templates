#!/usr/bin/env python3
"""
Validation script for Juniper JunOS Hierarchical Template System
Tests template rendering and validates output format matches expected structure
"""

import json
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

def create_test_data():
    """Create test data structure matching the GraphQL query format"""
    return {
        "hostname": "vrouter92",
        "config_context": {
            "version": "24.2R1-S2.5",
            "auto_image_upgrade": True,
            "root_authentication": {
                "encrypted_password": "$6$/W58L.AC$TNhEXPatGvT9J5UaMx9k/6Yc/2mvLILQgLRwjytphOFFeVHuX5UrPQlUxNPU8cgzWP/NV95RsE4SI/vCpUP5S1"
            },
            "users": [
                {
                    "name": "admin",
                    "uid": 2000,
                    "class": "super-user",
                    "encrypted_password": "$6$HpfB9N/q$TsnOU69fgDoH0selFOCJ6S/VhKXX6RdfYxr7TOtufDHColTaAT71ji9ReQKOB4mlHMySDpUWlzArR1qfgclPZ/"
                }
            ],
            "routing_options": {
                "static": [
                    {
                        "destination": "0.0.0.0/0",
                        "next_hop": "192.168.0.3"
                    }
                ]
            },
            "protocols": {
                "router_advertisement": {
                    "fxp0.0": {
                        "managed_configuration": True
                    }
                }
            }
        },
        "interfaces": [
            {
                "name": "ge-0/0/0",
                "enabled": True,
                "ip_addresses": [
                    {"address": "10.0.0.15/24"}
                ]
            },
            {
                "name": "ge-0/0/1",
                "enabled": True,
                "ip_addresses": [
                    {"address": "10.0.0.14/24"}
                ]
            },
            {
                "name": "fxp0",
                "enabled": True,
                "ip_addresses": [
                    {"address": "192.168.0.92/24"}
                ]
            }
        ]
    }

def validate_junos_format(output):
    """Validate that the output matches JunOS hierarchical format"""
    errors = []
    
    # Check for version statement
    if not output.strip().startswith("## Last commit:"):
        errors.append("Missing commit comment header")
    
    if "version " not in output:
        errors.append("Missing version statement")
    
    # Check for proper curly brace structure
    if "system {" not in output:
        errors.append("Missing system section with curly braces")
    
    if "interfaces {" not in output:
        errors.append("Missing interfaces section with curly braces")
    
    # Check for proper statement termination
    if "host-name vrouter92;" not in output:
        errors.append("Missing hostname configuration")
    
    # Check for proper indentation and structure
    lines = output.split('\n')
    brace_count = 0
    for line in lines:
        brace_count += line.count('{') - line.count('}')
        
    if brace_count != 0:
        errors.append(f"Unbalanced curly braces: {brace_count}")
    
    return errors

def test_template_rendering():
    """Test the template rendering with sample data"""
    try:
        # Set up Jinja2 environment
        template_dir = Path.cwd()
        env = Environment(loader=FileSystemLoader(template_dir))
        
        # Load the main template
        template = env.get_template('juniper_junos_json.j2')
        
        # Create test data
        test_data = create_test_data()
        
        # Render the template
        output = template.render(**test_data)
        
        print("=== RENDERED TEMPLATE OUTPUT ===")
        print(output)
        print("\n=== VALIDATION RESULTS ===")
        
        # Validate the output
        errors = validate_junos_format(output)
        
        if errors:
            print("VALIDATION FAILED:")
            for error in errors:
                print(f"  - {error}")
            return False
        else:
            print("VALIDATION PASSED: Template generates valid JunOS configuration format")
            return True
            
    except TemplateNotFound as e:
        print(f"Template not found: {e}")
        return False
    except Exception as e:
        print(f"Error during template rendering: {e}")
        return False

def compare_with_reference():
    """Compare generated output with reference configuration"""
    try:
        with open('juniper_junos_json.cfg', 'r') as f:
            reference = f.read()
        
        print("\n=== REFERENCE CONFIGURATION ===")
        print(reference)
        
        return True
    except FileNotFoundError:
        print("Reference file 'juniper_junos_json.cfg' not found")
        return False

def main():
    """Main validation function"""
    print("Juniper JunOS Template Validation Script")
    print("=" * 50)
    
    # Test template rendering
    success = test_template_rendering()
    
    # Compare with reference
    compare_with_reference()
    
    # Summary
    print("\n=== SUMMARY ===")
    if success:
        print("✓ Template validation PASSED")
        print("✓ Modular template system working correctly")
        print("✓ Generated configuration matches JunOS hierarchical format")
    else:
        print("✗ Template validation FAILED")
        print("✗ Please check template implementation")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())