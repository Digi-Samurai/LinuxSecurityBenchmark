import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_sudo_installed() -> Dict[str, Any]:
    """
    Ensure sudo is installed.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.2.1',
        'name': 'Ensure sudo is installed',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if sudo is installed
        sudo_check = subprocess.run(['which', 'sudo'], capture_output=True, text=True)
        
        if sudo_check.returncode == 0:
            result['status'] = True
            result['details'] = 'sudo is installed.'
            logger.info(result['details'])
        else:
            result['details'] = 'sudo is not installed.'
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking sudo installation: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'sudo_installed': check_sudo_installed()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
