import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_ip_forwarding() -> Dict[str, Any]:
    """
    Check if IP forwarding is disabled
    CIS Benchmark 3.3.1 - Ensure IP forwarding is disabled
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '3.3.1',
        'name': 'Ensure IP forwarding is disabled',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check IPv4 forwarding
        ipv4_forward_cmd = "sysctl net.ipv4.ip_forward"
        ipv4_result = subprocess.run(
            ipv4_forward_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check IPv6 forwarding
        ipv6_forward_cmd = "sysctl net.ipv6.conf.all.forwarding"
        ipv6_result = subprocess.run(
            ipv6_forward_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if forwarding is disabled (should be 0)
        ipv4_disabled = "net.ipv4.ip_forward = 0" in ipv4_result.stdout
        ipv6_disabled = "net.ipv6.conf.all.forwarding = 0" in ipv6_result.stdout
        
        if ipv4_disabled and ipv6_disabled:
            result['status'] = True
            result['details'] = 'IP forwarding is disabled for both IPv4 and IPv6'
            logger.info(result['details'])
        else:
            result['details'] = 'IP forwarding is enabled'
            logger.warning(result['details'])
            
            # Provide more specific information
            if not ipv4_disabled:
                result['details'] += '. IPv4 forwarding is enabled'
            if not ipv6_disabled:
                result['details'] += '. IPv6 forwarding is enabled'
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking IP forwarding: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'ip_forwarding': check_ip_forwarding()
    }
    
    return results

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Direct execution for testing
    results = run()
    print(results['ip_forwarding'])