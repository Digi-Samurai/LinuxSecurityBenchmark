import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_ufw_installed() -> Dict[str, Any]:
    """
    Check if UFW is installed
    CIS Benchmark 4.2.1 - Ensure ufw is installed
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '4.2.1',
        'name': 'Ensure ufw is installed',
        'status': False,
        'severity': 'high',
        'details': ''
    }
    
    try:
        # Check if ufw is installed
        ufw_check = subprocess.run(
            ['dpkg', '-s', 'ufw'], 
            capture_output=True, 
            text=True
        )
        
        # Check if package is installed and status is ok
        if ufw_check.returncode == 0 and 'Status: install ok installed' in ufw_check.stdout:
            result['status'] = True
            result['details'] = 'UFW is installed'
            logger.info('UFW is installed')
        else:
            result['details'] = 'UFW is not installed'
            logger.warning('UFW is not installed')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking UFW installation: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'ufw_installed': check_ufw_installed()
    }
    
    return results

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    results = run()
    print(results['ufw_installed'])