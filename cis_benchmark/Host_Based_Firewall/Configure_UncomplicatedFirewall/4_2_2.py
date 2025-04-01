import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_iptables_persistent() -> Dict[str, Any]:
    """
    Check if iptables-persistent is not installed
    CIS Benchmark 4.2.2 - Ensure iptables-persistent is not installed with ufw
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '4.2.2',
        'name': 'Ensure iptables-persistent is not installed',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check if iptables-persistent is installed
        iptables_check = subprocess.run(
            ['dpkg', '-s', 'iptables-persistent'], 
            capture_output=True, 
            text=True
        )
        
        # If package is not installed, it's compliant
        if iptables_check.returncode != 0:
            result['status'] = True
            result['details'] = 'Iptables-persistent is not installed'
            logger.info('Iptables-persistent is not installed')
        else:
            result['details'] = 'Iptables-persistent is installed'
            logger.warning('Iptables-persistent is installed')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking iptables-persistent: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'iptables_persistent': check_iptables_persistent()
    }
    
    return results

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    results = run()
    print(results['iptables_persistent'])