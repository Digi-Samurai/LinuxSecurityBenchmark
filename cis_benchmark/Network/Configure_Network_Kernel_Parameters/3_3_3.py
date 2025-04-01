import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_bogus_icmp_responses() -> Dict[str, Any]:
    """
    Check if bogus ICMP responses are ignored
    CIS Benchmark 3.3.3 - Ensure bogus ICMP responses are ignored
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '3.3.3',
        'name': 'Ensure bogus ICMP responses are ignored',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check for ignoring bogus error responses
        bogus_error_cmd = "sysctl net.ipv4.icmp_ignore_bogus_error_responses"
        
        bogus_error_result = subprocess.run(
            bogus_error_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if bogus error responses are ignored (should be 1)
        bogus_ignored = "net.ipv4.icmp_ignore_bogus_error_responses = 1" in bogus_error_result.stdout
        
        if bogus_ignored:
            result['status'] = True
            result['details'] = 'Bogus ICMP error responses are being ignored'
            logger.info(result['details'])
        else:
            result['details'] = 'Bogus ICMP error responses are not being ignored'
            logger.warning(result['details'])
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking bogus ICMP responses: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'bogus_icmp_responses': check_bogus_icmp_responses()
    }
    
    return results

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Direct execution for testing
    results = run()
    print(results['bogus_icmp_responses'])