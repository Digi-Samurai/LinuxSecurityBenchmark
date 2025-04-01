import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_source_routed_packets() -> Dict[str, Any]:
    """
    Check if source routed packets are not accepted
    CIS Benchmark 3.3.8 - Ensure source routed packets are not accepted
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '3.3.8',
        'name': 'Ensure source routed packets are not accepted',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check all and default interfaces for source routing
        all_accept_source_route_cmd = "sysctl net.ipv4.conf.all.accept_source_route"
        default_accept_source_route_cmd = "sysctl net.ipv4.conf.default.accept_source_route"
        
        all_source_route = subprocess.run(
            all_accept_source_route_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        default_source_route = subprocess.run(
            default_accept_source_route_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if both are set to 0 (disabled)
        if (all_source_route.stdout.strip() == "net.ipv4.conf.all.accept_source_route = 0" and
            default_source_route.stdout.strip() == "net.ipv4.conf.default.accept_source_route = 0"):
            result['status'] = True
            result['details'] = 'Source routed packets are disabled on all and default interfaces'
            logger.info(result['details'])
        else:
            result['details'] = 'Source routed packets are not fully disabled'
            logger.warning(result['details'])
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking source routed packets: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'source_routed_packets': check_source_routed_packets()
    }
    
    return results

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())