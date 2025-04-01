import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_pam_unix_nullok() -> Dict[str, Any]:
    """
    Ensure pam_unix does not include nullok.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.3.3.4.1',
        'name': 'Ensure pam_unix does not include nullok',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        with open('/etc/pam.d/common-password', 'r') as file:
            content = file.read().lower()

        if 'pam_unix.so' in content and 'nullok' in content:
            result['details'] = "pam_unix includes nullok, which allows empty passwords."
            logger.warning(result['details'])
        else:
            result['status'] = True
            result['details'] = "pam_unix does not include nullok."
            logger.info(result['details'])

    except Exception as e:
        result['details'] = f"Error checking pam_unix nullok setting: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'pam_unix_nullok': check_pam_unix_nullok()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
