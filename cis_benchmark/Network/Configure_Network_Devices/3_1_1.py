import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_ipv6_status() -> Dict[str, Any]:
    """
    Identify IPv6 status (Manual Check)
    CIS Benchmark 3.1.1 - Ensure IPv6 status is identified
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '3.1.1',
        'name': 'Ensure IPv6 status is identified',
        'status': 'MANUAL',
        'severity': 'medium',
        'details': 'Manual verification required',
        'ipv6_interfaces': [],
        'ipv6_enabled_interfaces': []
    }
    
    try:
        # Get all network interfaces
        interfaces_cmd = "ip -6 addr"
        interfaces_result = subprocess.run(
            interfaces_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Get kernel IPv6 settings
        sysctl_cmd = "sysctl net.ipv6.conf.all.disable_ipv6"
        sysctl_result = subprocess.run(
            sysctl_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Collect IPv6 interfaces
        if interfaces_result.stdout:
            # Parse interfaces from the output
            interfaces = [line.split()[-1] for line in interfaces_result.stdout.split('\n') if 'inet6' in line]
            result['ipv6_interfaces'] = list(set(interfaces))
        
        # Check IPv6 kernel settings
        result['ipv6_kernel_status'] = sysctl_result.stdout.strip()
        
        # Detailed explanation for manual review
        result['details'] = (
            "IPv6 Status Identification:\n"
            f"Kernel IPv6 Setting: {result['ipv6_kernel_status']}\n"
            f"IPv6 Interfaces Found: {', '.join(result['ipv6_interfaces'])}\n"
            "MANUAL VERIFICATION REQUIRED:\n"
            "1. Review the IPv6 interfaces and kernel settings\n"
            "2. Determine if IPv6 is necessary for your environment\n"
            "3. Decide whether to disable or keep IPv6"
        )
        
        logger.info("IPv6 status identification completed")
    
    except Exception as e:
        result['status'] = 'ERROR'
        result['details'] = f'Error identifying IPv6 status: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'ipv6_status': check_ipv6_status()
    }
    
    return results

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Direct execution for testing
    results = run()
    print(results['ipv6_status']['details'])