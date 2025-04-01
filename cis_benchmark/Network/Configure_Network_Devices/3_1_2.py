import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_wireless_interfaces() -> Dict[str, Any]:
    """
    Check if wireless interfaces are disabled
    CIS Benchmark 3.1.2 - Ensure wireless interfaces are disabled
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '3.1.2',
        'name': 'Ensure wireless interfaces are disabled',
        'status': False,
        'severity': 'medium',
        'details': '',
        'wireless_interfaces': []
    }
    
    try:
        # Command to find wireless interfaces
        wireless_interfaces_cmd = "iwconfig 2>/dev/null | grep -E '^[a-z]' | awk '{print $1}'"
        wireless_interfaces_result = subprocess.run(
            wireless_interfaces_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Alternative method using ip command
        alt_wireless_interfaces_cmd = "ip link show | grep -i 'wlan\|wifi\|wireless'"
        alt_interfaces_result = subprocess.run(
            alt_wireless_interfaces_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Combine and deduplicate interfaces
        wireless_interfaces = set()
        
        # Parse iwconfig results
        if wireless_interfaces_result.stdout:
            wireless_interfaces.update(
                line.strip() for line in wireless_interfaces_result.stdout.split('\n') if line.strip()
            )
        
        # Parse alternative method results
        if alt_interfaces_result.stdout:
            wireless_interfaces.update(
                line.split(':')[1].strip() for line in alt_interfaces_result.stdout.split('\n') 
                if line.strip() and ':' in line
            )
        
        # Store found interfaces
        result['wireless_interfaces'] = list(wireless_interfaces)
        
        # Determine compliance
        if not wireless_interfaces:
            result['status'] = True
            result['details'] = 'No wireless interfaces found'
        else:
            result['details'] = f'Wireless interfaces found: {", ".join(wireless_interfaces)}'
        
        logger.info(result['details'])
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking wireless interfaces: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'wireless_interfaces': check_wireless_interfaces()
    }
    
    return results

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Direct execution for testing
    results = run()
    print(results['wireless_interfaces'])