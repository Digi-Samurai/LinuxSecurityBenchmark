import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_reverse_path_filtering() -> Dict[str, Any]:
    """
    Check if reverse path filtering is enabled
    CIS Benchmark 3.3.7 - Ensure reverse path filtering is enabled
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '3.3.7',
        'name': 'Ensure reverse path filtering is enabled',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check all and default interfaces for reverse path filtering
        all_rpfilter_cmd = "sysctl net.ipv4.conf.all.rp_filter"
        default_rpfilter_cmd = "sysctl net.ipv4.conf.default.rp_filter"
        
        all_rpfilter = subprocess.run(
            all_rpfilter_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        default_rpfilter = subprocess.run(
            default_rpfilter_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if both are set to 1 (enabled)
        if (all_rpfilter.stdout.strip() == "net.ipv4.conf.all.rp_filter = 1" and
            default_rpfilter.stdout.strip() == "net.ipv4.conf.default.rp_filter = 1"):
            result['status'] = True
            result['details'] = 'Reverse path filtering is enabled on all and default interfaces'
            logger.info(result['details'])
        else:
            result['details'] = 'Reverse path filtering is not fully enabled'
            logger.warning(result['details'])
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking reverse path filtering: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'reverse_path_filtering': check_reverse_path_filtering()
    }
    
    return results

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())