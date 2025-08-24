# Juniper JunOS JSON Template System

## Overview

This directory contains a modular Jinja2 template system for generating JSON-style configurations for Juniper devices. The templates generate configurations compatible with JunOS REST API specifications, enabling programmatic device configuration through JSON payloads.

The system builds upon the existing CLI template implementation while introducing a completely separate modular architecture that generates JSON output instead of CLI commands.

## Directory Structure

```
├── juniper_junos_json.j2          # Main orchestration template
├── junos_json/                    # JSON template modules directory
│   ├── _system.j2                 # System configuration orchestrator
│   ├── _interfaces.j2             # Interface configuration orchestrator  
│   ├── _protocols.j2              # Protocol configuration orchestrator
│   ├── _services.j2               # Services configuration orchestrator
│   ├── _security.j2               # Security configuration orchestrator
│   │
│   ├── _hostname.j2               # System hostname configuration
│   ├── _dns.j2                    # DNS configuration
│   ├── _ntp.j2                    # NTP configuration
│   ├── _users.j2                  # User management configuration
│   ├── _ssh.j2                    # SSH service configuration
│   ├── _syslog.j2                 # System logging configuration
│   │
│   ├── _physical_interface.j2     # Physical interface (ge-*) configuration
│   ├── _management_interface.j2   # Management interface (fxp0) configuration
│   ├── _loopback_interface.j2     # Loopback interface configuration
│   ├── _vlan_interface.j2         # VLAN interface configuration
│   ├── _aggregated_interface.j2   # Link aggregation configuration
│   │
│   ├── _bgp.j2                    # BGP protocol configuration
│   ├── _ospf.j2                   # OSPF protocol configuration
│   ├── _lldp.j2                   # LLDP protocol configuration
│   ├── _static_routes.j2          # Static routing configuration
│   │
│   ├── _snmp.j2                   # SNMP service configuration
│   ├── _dhcp.j2                   # DHCP service configuration
│   ├── _web_management.j2         # Web management configuration
│   │
│   ├── _firewall.j2               # Firewall rules configuration
│   ├── _zones.j2                  # Security zones configuration
│   └── _policies.j2               # Security policies configuration
└── validate_json_templates.py     # Validation and testing script
```

## Template Hierarchy

The template system follows a hierarchical modular design:

```
juniper_junos_json.j2 (Main Template)
├── System Module (_system.j2)
│   ├── _hostname.j2
│   ├── _dns.j2
│   ├── _ntp.j2
│   ├── _users.j2
│   ├── _ssh.j2
│   └── _syslog.j2
├── Interfaces Module (_interfaces.j2)
│   ├── _physical_interface.j2
│   ├── _management_interface.j2
│   ├── _loopback_interface.j2
│   ├── _vlan_interface.j2
│   └── _aggregated_interface.j2
├── Protocols Module (_protocols.j2)
│   ├── _bgp.j2
│   ├── _ospf.j2
│   ├── _lldp.j2
│   └── _static_routes.j2
├── Services Module (_services.j2)
│   ├── _snmp.j2
│   ├── _dhcp.j2
│   └── _web_management.j2
└── Security Module (_security.j2)
    ├── _firewall.j2
    ├── _zones.j2
    └── _policies.j2
```

## Data Structure Compatibility

The JSON templates use the same GraphQL data structure as the CLI templates:

### Required Variables
- `hostname`: Device hostname (string)
- `interfaces`: List of interface configurations
- `config_context`: Device-specific configuration context
- `snmp`: SNMP configuration flag (boolean)

### Sample Data Structure
```json
{
  "hostname": "router.example.com",
  "interfaces": [
    {
      "name": "ge-0/0/0",
      "description": "WAN Interface",
      "enabled": true,
      "ip_addresses": [{"address": "192.168.1.1/24"}]
    }
  ],
  "config_context": {
    "bgp": {
      "asn": 65001,
      "neighbors": [{"ip": "192.168.1.2", "remote-asn": 65002}]
    },
    "lldp": true,
    "snmp": [{"name": "public", "role": "read-only"}]
  },
  "snmp": true
}
```

## Generated JSON Structure

The templates generate JSON conforming to JunOS REST API schema:

```json
{
  "configuration": {
    "system": {
      "host-name": "device-name",
      "root-authentication": {...},
      "login": {...},
      "services": {...},
      "syslog": {...}
    },
    "interfaces": {
      "interface": [...]
    },
    "protocols": {
      "bgp": {...},
      "lldp": {...}
    },
    "services": {
      "snmp": {...}
    },
    "security": {
      "zones": {...},
      "policies": {...}
    }
  }
}
```

## Usage Examples

### Basic Usage with Jinja2

```python
from jinja2 import Environment, FileSystemLoader

# Setup template environment
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('juniper_junos_json.j2')

# Render configuration
config_json = template.render(
    hostname="test-router.example.com",
    interfaces=[...],
    config_context={...},
    snmp=True
)

# Parse and validate JSON
import json
config = json.loads(config_json)
```

### Integration with Nautobot Golden Config

1. Place `juniper_junos_json.j2` in your Golden Config template directory
2. Configure template mapping for Juniper devices
3. Use existing GraphQL query and transposer
4. Templates will generate JSON instead of CLI commands

## Configuration Features

### System Configuration
- **Hostname**: Automatically extracts short hostname from FQDN
- **User Management**: Supports multiple users with encrypted passwords
- **DNS**: Configurable domain and name servers
- **NTP**: Configurable NTP servers with fallback defaults
- **SSH**: Enables SSH service for management access
- **Syslog**: Configures system logging with standard files

### Interface Configuration
- **Physical Interfaces**: GigabitEthernet (ge-*) interfaces
- **Management Interfaces**: Management interface (fxp0) configuration
- **Loopback Interfaces**: Loopback interface configuration
- **VLAN Interfaces**: VLAN tagging and interface configuration
- **Aggregated Interfaces**: Link aggregation with LACP

### Protocol Configuration
- **BGP**: Border Gateway Protocol with neighbor configuration
- **OSPF**: Open Shortest Path First (extensible for areas)
- **LLDP**: Link Layer Discovery Protocol
- **Static Routes**: Static routing configuration

### Service Configuration
- **SNMP**: Community-based SNMP with view configuration
- **DHCP**: DHCP local server with pool configuration
- **Web Management**: HTTP/HTTPS management interface

### Security Configuration
- **Firewall**: Packet filtering rules with terms
- **Security Zones**: Network security zones with interfaces
- **Security Policies**: Inter-zone security policies

## Template Development

### Adding New Modules

1. Create partial template in `junos_json/` directory
2. Follow naming convention: `_module_name.j2`
3. Generate valid JSON fragments
4. Include in appropriate orchestrator template
5. Test with validation script

### JSON Structure Guidelines

- Use proper JSON syntax with correct quoting
- Handle conditional sections with Jinja2 logic
- Include trailing commas correctly for arrays/objects
- Validate JSON output for syntax correctness

### Testing Templates

Use the included validation script:

```bash
python validate_json_templates.py
```

This script:
- Validates modular structure completeness
- Tests template rendering with sample data
- Validates generated JSON syntax
- Reports any errors or issues

## Differences from CLI Templates

| Aspect | CLI Templates | JSON Templates |
|--------|---------------|----------------|
| **Output Format** | CLI commands (`set ...`) | JSON objects |
| **Directory** | `junos/` | `junos_json/` |
| **Main Template** | `juniper_junos.j2` | `juniper_junos_json.j2` |
| **API Compatibility** | CLI/SSH | REST API |
| **Data Structure** | Same GraphQL data | Same GraphQL data |
| **Modularity** | Partial templates | Modular JSON fragments |

## Validation and Testing

The template system includes comprehensive validation:

### Structural Validation
- Verifies all required template files exist
- Checks modular organization
- Validates file naming conventions

### Syntax Validation
- Tests Jinja2 template rendering
- Validates JSON syntax correctness
- Checks for template logic errors

### Integration Testing
- Tests with sample device data
- Validates complete configuration generation
- Ensures JunOS schema compliance

## Best Practices

1. **Modular Development**: Keep templates focused on single configuration aspects
2. **Error Handling**: Include appropriate checks for missing data
3. **JSON Validity**: Always validate generated JSON syntax
4. **Testing**: Test templates with various data scenarios
5. **Documentation**: Document template variables and data structures

## Troubleshooting

### Common Issues

**Template Rendering Errors**
- Check Jinja2 syntax in templates
- Verify variable names match data structure
- Ensure proper conditional logic

**JSON Syntax Errors**
- Validate JSON structure manually
- Check for missing/extra commas
- Verify proper string quoting

**Missing Configuration**
- Check conditional logic in templates
- Verify data structure contains expected fields
- Test with validation script

### Debugging Tips

1. Use the validation script to identify issues
2. Test templates with minimal data first
3. Validate JSON syntax after any changes
4. Check template include paths and file names

## Support and Extension

The modular design allows easy extension for new features:

- Add new partial templates for additional configuration elements
- Extend existing modules with new functionality
- Create vendor-specific variations
- Integrate with custom data sources

For additional configuration requirements, follow the established patterns and maintain the modular structure for consistency and maintainability.