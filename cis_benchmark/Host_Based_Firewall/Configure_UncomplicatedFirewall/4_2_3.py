import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_ufw_service_enabled() -> Dict[str, Any]:
    """
    Check if UFW service is enabled
    CIS Benchmark 4.2.3 - Ensure ufw service is enabled
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '4.2.3',
        'name': 'Ensure ufw service is enabled',
        'status': False,
        'severity': 'high',
        'details': ''
    }
    
    try:
        # Check UFW service status
        ufw_status = subprocess.run(
            ['systemctl', 'is-enabled', 'ufw'], 
            capture_output=True, 
            text=True
        )
        
        # Check if service is active
        ufw_active = subprocess.run(
            ['systemctl', 'is-active', 'ufw'], 
            capture_output=True, 
            text=True
        )
        
        # Check if service is enabled and active
        if ufw_status.returncode == 0 and ufw_active.returncode == 0:
            result['status'] = True
            result['details'] = 'UFW service is enabled and active'
            logger.info('UFW service is enabled and active')
        else:
            result['details'] = 'UFW service is not enabled or active'
            logger.warning('UFW service is not enabled or active')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking UFW service status: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'ufw_service': check_ufw_service_enabled()
    }
    
    return results

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    results = run()
    print(results['ufw_service'])