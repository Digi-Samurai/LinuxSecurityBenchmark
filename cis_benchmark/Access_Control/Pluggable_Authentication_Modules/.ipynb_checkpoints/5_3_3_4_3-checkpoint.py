import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_pam_unix_hashing() -> Dict[str, Any]:
    """
    Ensure pam_unix includes a strong password hashing algorithm.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.3.3.4.3',
        'name': 'Ensure pam_unix includes a strong password hashing algorithm',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        with open('/etc/pam.d/common-password', 'r') as file:
            content = file.read().lower()

        if 'pam_unix.so' in content and ('sha512' in content or 'yescrypt' in content):
            result['status'] = True
            result['details'] = "pam_unix uses a strong password hashing algorithm."
            logger.info(result['details'])
        else:
            result['details'] = "pam_unix does not specify a strong password hashing algorithm."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking pam_unix hashing algorithm: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'pam_unix_hashing': check_pam_unix_hashing()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
