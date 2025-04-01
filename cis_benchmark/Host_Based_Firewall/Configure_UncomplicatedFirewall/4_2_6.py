import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def get_open_ports() -> set:
    """Get open TCP and UDP ports using 'ss' command."""
    open_ports = set()
    
    try:
        result = subprocess.run(
            ["ss", "-tuln"], capture_output=True, text=True
        )
        lines = result.stdout.splitlines()
        
        for line in lines[1:]:  # Skip header
            parts = line.split()
            if len(parts) >= 5:
                port = parts[4].split(":")[-1]
                if port.isdigit():
                    open_ports.add(int(port))
        
    except Exception as e:
        logger.error(f"Error retrieving open ports: {e}")
    
    return open_ports

def get_ufw_allowed_ports() -> set:
    """Get all allowed UFW ports, ignoring errors if UFW is missing."""
    allowed_ports = set()
    
    try:
        result = subprocess.run(
            ["ufw", "status", "numbered"], capture_output=True, text=True, check=True
        )
        lines = result.stdout.lower().splitlines()
        
        for line in lines:
            parts = line.split()
            for part in parts:
                if "/" in part:  # Example: '22/tcp'
                    port = part.split("/")[0]
                    if port.isdigit():
                        allowed_ports.add(int(port))
    
    except FileNotFoundError:
        # UFW is not installed, return empty set without logging an error
        return set()
    
    except Exception as e:
        logger.error(f"Error retrieving UFW rules: {e}")
    
    return allowed_ports

def check_ufw_rules_for_open_ports() -> Dict[str, Any]:
    """Check if UFW rules exist for all open ports."""
    result = {
        'benchmark_id': '4.2.6',
        'name': 'Ensure UFW rules exist for all open ports',
        'status': False,
        'severity': 'high',
        'details': ''
    }
    
    open_ports = get_open_ports()
    ufw_ports = get_ufw_allowed_ports()
    
    missing_rules = open_ports - ufw_ports
    
    if not missing_rules:
        result['status'] = True
        result['details'] = 'All open ports have corresponding UFW rules.'
    else:
        result['details'] = f'Missing UFW rules for ports: {sorted(missing_rules)}'
        logger.warning(result['details'])  # Only log this warning
    
    return result

def run():
    """Run all checks for this benchmark section."""
    results = {
        'ufw_open_ports': check_ufw_rules_for_open_ports()
    }
    return results

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
    
    results = run()
