import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_same_consecutive_characters() -> Dict[str, Any]:
    """
    Ensure password same consecutive characters is configured.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.3.3.2.4',
        'name': 'Ensure password same consecutive characters is configured',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check for same consecutive characters configuration in /etc/security/pwquality.conf
        with open('/etc/security/pwquality.conf', 'r') as file:
            content = file.read().lower()
        
        if 'maxrepeat' in content:
            result['status'] = True
            result['details'] = "Password same consecutive characters is configured."
            logger.info(result['details'])
        else:
            result['details'] = "Password same consecutive characters is not configured."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking same consecutive characters: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'same_consecutive_chars_config': check_same_consecutive_characters()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
