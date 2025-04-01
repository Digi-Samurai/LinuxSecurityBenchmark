import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_pam_pwhistory_use_authtok() -> Dict[str, Any]:
    """
    Ensure pam_pwhistory includes use_authtok.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.3.3.3.3',
        'name': 'Ensure pam_pwhistory includes use_authtok',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        with open('/etc/pam.d/common-password', 'r') as file:
            content = file.read().lower()

        if 'pam_pwhistory.so' in content and 'use_authtok' in content:
            result['status'] = True
            result['details'] = "pam_pwhistory includes use_authtok."
            logger.info(result['details'])
        else:
            result['details'] = "pam_pwhistory does not include use_authtok."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking pam_pwhistory use_authtok setting: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'pam_pwhistory_use_authtok': check_pam_pwhistory_use_authtok()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
