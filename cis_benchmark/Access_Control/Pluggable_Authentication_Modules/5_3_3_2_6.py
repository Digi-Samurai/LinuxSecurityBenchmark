import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_dictionary_check() -> Dict[str, Any]:
    """
    Ensure password dictionary check is enabled.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.3.3.2.6',
        'name': 'Ensure password dictionary check is enabled',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if dictionary check is enabled in /etc/pam.d/common-password
        with open('/etc/pam.d/common-password', 'r') as pam_file:
            content = pam_file.read().lower()
        
        if 'pam_pwquality.so' in content and 'dictcheck' in content:
            result['status'] = True
            result['details'] = "Password dictionary check is enabled."
            logger.info(result['details'])
        else:
            result['details'] = "Password dictionary check is not enabled."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking dictionary check: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'password_dictionary_check': check_dictionary_check()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
