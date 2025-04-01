import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_pam_unix_remember() -> Dict[str, Any]:
    """
    Ensure pam_unix does not include remember.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.3.3.4.2',
        'name': 'Ensure pam_unix does not include remember',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        with open('/etc/pam.d/common-password', 'r') as file:
            content = file.read().lower()

        if 'pam_unix.so' in content and 'remember=' in content:
            result['details'] = "pam_unix includes remember, which should be handled by pam_pwhistory."
            logger.warning(result['details'])
        else:
            result['status'] = True
            result['details'] = "pam_unix does not include remember."
            logger.info(result['details'])

    except Exception as e:
        result['details'] = f"Error checking pam_unix remember setting: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'pam_unix_remember': check_pam_unix_remember()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
