import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_secure_icmp_redirects() -> Dict[str, Any]:
    """
    Check if secure ICMP redirects are not accepted
    CIS Benchmark 3.3.6 - Ensure secure ICMP redirects are not accepted
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '3.3.6',
        'name': 'Ensure secure ICMP redirects are not accepted',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check all interfaces for ICMP redirect acceptance
        all_redirects_cmd = "sysctl net.ipv4.conf.all.secure_redirects"
        default_redirects_cmd = "sysctl net.ipv4.conf.default.secure_redirects"
        
        all_redirects = subprocess.run(
            all_redirects_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        default_redirects = subprocess.run(
            default_redirects_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if both are set to 0 (disabled)
        if (all_redirects.stdout.strip() == "net.ipv4.conf.all.secure_redirects = 0" and
            default_redirects.stdout.strip() == "net.ipv4.conf.default.secure_redirects = 0"):
            result['status'] = True
            result['details'] = 'Secure ICMP redirects are disabled on all and default interfaces'
            logger.info(result['details'])
        else:
            result['details'] = 'Secure ICMP redirects are not fully disabled'
            logger.warning(result['details'])
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking ICMP redirects: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'secure_icmp_redirects': check_secure_icmp_redirects()
    }
    
    return results

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())