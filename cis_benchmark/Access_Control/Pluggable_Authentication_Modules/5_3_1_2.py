import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_libpam_modules_installed() -> Dict[str, Any]:
    """
    Ensure libpam-modules is installed.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.3.1.2',
        'name': 'Ensure libpam-modules is installed',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check for libpam-modules package installation
        pam_modules_check = subprocess.run(['dpkg', '-l', 'libpam-modules'], capture_output=True, text=True)
        
        if pam_modules_check.returncode == 0:
            result['status'] = True
            result['details'] = "libpam-modules is installed."
            logger.info(result['details'])
        else:
            result['details'] = "libpam-modules is not installed."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking libpam-modules installation: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'libpam_modules_installed': check_libpam_modules_installed()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
