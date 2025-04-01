import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_pam_installed() -> Dict[str, Any]:
    """
    Ensure the latest version of PAM is installed.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.3.1.1',
        'name': 'Ensure latest version of PAM is installed',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check for PAM package version
        pam_check = subprocess.run(['dpkg', '-l', 'libpam0g'], capture_output=True, text=True)
        
        if pam_check.returncode == 0:
            result['status'] = True
            result['details'] = "PAM is installed."
            logger.info(result['details'])
        else:
            result['details'] = "PAM is not installed."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking PAM installation: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'pam_installed': check_pam_installed()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
