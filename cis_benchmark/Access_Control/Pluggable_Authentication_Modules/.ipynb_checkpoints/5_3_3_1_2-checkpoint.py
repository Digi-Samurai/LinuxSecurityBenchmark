import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_password_unlock_time() -> Dict[str, Any]:
    """
    Ensure password unlock time is configured.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.3.3.1.2',
        'name': 'Ensure password unlock time is configured',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check for pam_faillock unlock time setting in /etc/pam.d/common-auth or similar files
        with open('/etc/pam.d/common-auth', 'r') as pam_file:
            pam_content = pam_file.read().lower()
        
        if 'unlock_time' in pam_content:
            result['status'] = True
            result['details'] = "Password unlock time is configured."
            logger.info(result['details'])
        else:
            result['details'] = "Password unlock time is not configured."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking password unlock time: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'password_unlock_time': check_password_unlock_time()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
