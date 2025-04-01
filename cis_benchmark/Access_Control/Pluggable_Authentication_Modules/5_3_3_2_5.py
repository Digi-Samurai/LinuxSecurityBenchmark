import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_max_sequential_characters() -> Dict[str, Any]:
    """
    Ensure password maximum sequential characters is configured.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.3.3.2.5',
        'name': 'Ensure password maximum sequential characters is configured',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check for maximum sequential characters configuration in /etc/security/pwquality.conf
        with open('/etc/security/pwquality.conf', 'r') as file:
            content = file.read().lower()
        
        if 'maxsequence' in content:
            result['status'] = True
            result['details'] = "Password maximum sequential characters is configured."
            logger.info(result['details'])
        else:
            result['details'] = "Password maximum sequential characters is not configured."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking maximum sequential characters: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'max_sequential_chars_config': check_max_sequential_characters()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
