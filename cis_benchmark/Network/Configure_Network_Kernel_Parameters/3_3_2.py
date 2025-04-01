import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_packet_redirect_sending() -> Dict[str, Any]:
    """
    Check if packet redirect sending is disabled
    CIS Benchmark 3.3.2 - Ensure packet redirect sending is disabled
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '3.3.2',
        'name': 'Ensure packet redirect sending is disabled',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check all interfaces for send_redirects
        all_send_redirects_cmd = "sysctl net.ipv4.conf.all.send_redirects"
        default_send_redirects_cmd = "sysctl net.ipv4.conf.default.send_redirects"
        
        all_result = subprocess.run(
            all_send_redirects_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        default_result = subprocess.run(
            default_send_redirects_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if send_redirects is disabled (should be 0)
        all_disabled = "net.ipv4.conf.all.send_redirects = 0" in all_result.stdout
        default_disabled = "net.ipv4.conf.default.send_redirects = 0" in default_result.stdout
        
        if all_disabled and default_disabled:
            result['status'] = True
            result['details'] = 'Packet redirect sending is disabled for all and default interfaces'
            logger.info(result['details'])
        else:
            result['details'] = 'Packet redirect sending is enabled'
            logger.warning(result['details'])
            
            # Provide more specific information
            if not all_disabled:
                result['details'] += '. All interfaces send redirects'
            if not default_disabled:
                result['details'] += '. Default interface sends redirects'
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking packet redirect sending: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'packet_redirect_sending': check_packet_redirect_sending()
    }
    
    return results

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Direct execution for testing
    results = run()
    print(results['packet_redirect_sending'])