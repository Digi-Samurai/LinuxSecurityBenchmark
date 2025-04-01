import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_ipv6_router_advertisements() -> Dict[str, Any]:
    """
    Check if IPv6 router advertisements are not accepted
    CIS Benchmark 3.3.11 - Ensure IPv6 router advertisements are not accepted
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '3.3.11',
        'name': 'Ensure IPv6 router advertisements are not accepted',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check all and default interfaces for IPv6 router advertisements
        all_accept_ra_cmd = "sysctl net.ipv6.conf.all.accept_ra"
        default_accept_ra_cmd = "sysctl net.ipv6.conf.default.accept_ra"
        
        all_accept_ra = subprocess.run(
            all_accept_ra_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        default_accept_ra = subprocess.run(
            default_accept_ra_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if both are set to 0 (disabled)
        if (all_accept_ra.stdout.strip() == "net.ipv6.conf.all.accept_ra = 0" and
            default_accept_ra.stdout.strip() == "net.ipv6.conf.default.accept_ra = 0"):
            result['status'] = True
            result['details'] = 'IPv6 router advertisements are disabled on all and default interfaces'
            logger.info(result['details'])
        else:
            result['details'] = 'IPv6 router advertisements are not fully disabled'
            logger.warning(result['details'])
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking IPv6 router advertisements: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'ipv6_router_advertisements': check_ipv6_router_advertisements()
    }
    
    return results

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())