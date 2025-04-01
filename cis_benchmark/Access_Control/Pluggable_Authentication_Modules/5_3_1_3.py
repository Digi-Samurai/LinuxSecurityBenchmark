import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_libpam_pwquality_installed() -> Dict[str, Any]:
    """
    Ensure libpam-pwquality is installed.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.3.1.3',
        'name': 'Ensure libpam-pwquality is installed',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check for libpam-pwquality package installation
        pam_pwquality_check = subprocess.run(['dpkg', '-l', 'libpam-pwquality'], capture_output=True, text=True)
        
        if pam_pwquality_check.returncode == 0:
            result['status'] = True
            result['details'] = "libpam-pwquality is installed."
            logger.info(result['details'])
        else:
            result['details'] = "libpam-pwquality is not installed."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking libpam-pwquality installation: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'libpam_pwquality_installed': check_libpam_pwquality_installed()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
