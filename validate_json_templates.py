#!/usr/bin/env python3
"""
JSON Template Validation Script for Juniper JunOS JSON Templates

This script demonstrates the modular Jinja2 template system for generating
JSON-style configurations for Juniper devices.
"""

import json
from jinja2 import Environment, FileSystemLoader
import os

def test_template_rendering():
    """Test the JSON template rendering with sample data."""
    
    # Setup Jinja2 environment
    template_dir = os.getcwd()
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # Sample data structure based on GraphQL query format
    sample_data = {
        "hostname": "test-router.example.com",
        "interfaces": [
            {
                "name": "ge-0/0/0",
                "description": "WAN Interface",
                "enabled": True,
                "ip_addresses": [
                    {"address": "192.168.1.1/24"}
                ]
            },
            {
                "name": "fxp0",
                "description": "Management Interface", 
                "enabled": True,
                "ip_addresses": [
                    {"address": "10.0.0.1/24"}
                ]
            },
            {
                "name": "lo0",
                "description": "Loopback Interface",
                "enabled": True,
                "ip_addresses": [
                    {"address": "1.1.1.1/32"}
                ]
            }
        ],
        "config_context": {
            "bgp": {
                "asn": 65001,
                "neighbors": [
                    {
                        "ip": "192.168.1.2",
                        "remote-asn": 65002
                    }
                ]
            },
            "lldp": True,
            "snmp": [
                {
                    "name": "public",
                    "role": "read-only"
                }
            ]
        },
        "snmp": True
    }
    
    try:
        # Load and render the main template
        template = env.get_template('juniper_junos_json.j2')
        rendered_config = template.render(**sample_data)
        
        # Validate JSON syntax
        parsed_json = json.loads(rendered_config)
        
        print("✅ Template rendered successfully!")
        print("✅ JSON syntax is valid!")
        print("\n" + "="*60)
        print("SAMPLE GENERATED CONFIGURATION:")
        print("="*60)
        print(json.dumps(parsed_json, indent=2))
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON syntax error: {e}")
        print(f"Rendered content: {rendered_config}")
        return False
    except Exception as e:
        print(f"❌ Template rendering error: {e}")
        return False

def validate_modular_structure():
    """Validate that all modular components exist."""
    
    required_files = [
        'juniper_junos_json.j2',
        'junos_json/_system.j2',
        'junos_json/_interfaces.j2', 
        'junos_json/_protocols.j2',
        'junos_json/_services.j2',
        'junos_json/_security.j2',
        'junos_json/_hostname.j2',
        'junos_json/_dns.j2',
        'junos_json/_ntp.j2',
        'junos_json/_users.j2',
        'junos_json/_physical_interface.j2',
        'junos_json/_management_interface.j2',
        'junos_json/_loopback_interface.j2',
        'junos_json/_bgp.j2',
        'junos_json/_lldp.j2',
        'junos_json/_snmp.j2'
    ]
    
    print("📁 MODULAR STRUCTURE VALIDATION:")
    print("="*60)
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing {len(missing_files)} required files")
        return False
    else:
        print(f"\n✅ All {len(required_files)} required files present")
        return True

if __name__ == "__main__":
    print("JUNIPER JUNOS JSON TEMPLATE VALIDATION")
    print("="*60)
    
    # Validate modular structure
    structure_valid = validate_modular_structure()
    
    print("\n")
    
    # Test template rendering
    if structure_valid:
        rendering_valid = test_template_rendering()
        
        if rendering_valid:
            print("\n🎉 VALIDATION SUCCESSFUL!")
            print("The modular JSON template system is ready for use.")
        else:
            print("\n❌ VALIDATION FAILED!")
            print("Template rendering issues detected.")
    else:
        print("❌ VALIDATION FAILED!")
        print("Missing required template files.")