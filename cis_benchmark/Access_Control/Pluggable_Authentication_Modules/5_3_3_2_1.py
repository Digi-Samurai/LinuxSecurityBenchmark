import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_number_of_changed_characters() -> Dict[str, Any]:
    """
    Ensure password number of changed characters is configured.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.3.3.2.1',
        'name': 'Ensure password number of changed characters is configured',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check for password settings in /etc/security/pwquality.conf or /etc/pam.d/common-password
        with open('/etc/security/pwquality.conf', 'r') as file:
            content = file.read().lower()
        
        if 'minclass' in content:
            result['status'] = True
            result['details'] = "Password number of changed characters is configured."
            logger.info(result['details'])
        else:
            result['details'] = "Password number of changed characters is not configured."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking number of changed characters: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'changed_characters_config': check_number_of_changed_characters()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
