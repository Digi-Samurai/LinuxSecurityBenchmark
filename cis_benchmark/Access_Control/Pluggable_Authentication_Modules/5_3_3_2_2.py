import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_minimum_password_length() -> Dict[str, Any]:
    """
    Ensure minimum password length is configured.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.3.3.2.2',
        'name': 'Ensure minimum password length is configured',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check for password length configuration in /etc/pam.d/common-password or /etc/security/pwquality.conf
        with open('/etc/security/pwquality.conf', 'r') as file:
            content = file.read().lower()
        
        if 'minlen' in content:
            result['status'] = True
            result['details'] = "Minimum password length is configured."
            logger.info(result['details'])
        else:
            result['details'] = "Minimum password length is not configured."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking minimum password length: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'min_password_length_config': check_minimum_password_length()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
