import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_broadcast_icmp_requests() -> Dict[str, Any]:
    """
    Check if broadcast ICMP requests are ignored
    CIS Benchmark 3.3.4 - Ensure broadcast ICMP requests are ignored
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '3.3.4',
        'name': 'Ensure broadcast ICMP requests are ignored',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check for ignoring broadcast ICMP requests
        all_broadcast_cmd = "sysctl net.ipv4.icmp_echo_ignore_broadcasts"
        
        broadcast_result = subprocess.run(
            all_broadcast_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if broadcast ICMP requests are ignored (should be 1)
        broadcast_ignored = "net.ipv4.icmp_echo_ignore_broadcasts = 1" in broadcast_result.stdout
        
        if broadcast_ignored:
            result['status'] = True
            result['details'] = 'Broadcast ICMP requests are being ignored'
            logger.info(result['details'])
        else:
            result['details'] = 'Broadcast ICMP requests are not being ignored'
            logger.warning(result['details'])
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking broadcast ICMP requests: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'broadcast_icmp_requests': check_broadcast_icmp_requests()
    }
    
    return results

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Direct execution for testing
    results = run()
    print(results['broadcast_icmp_requests'])