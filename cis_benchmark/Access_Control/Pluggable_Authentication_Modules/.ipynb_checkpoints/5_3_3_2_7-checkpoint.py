import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_password_quality_enforced() -> Dict[str, Any]:
    """
    Ensure password quality checking is enforced.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.3.3.2.7',
        'name': 'Ensure password quality checking is enforced',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if pwquality module is enabled in PAM settings
        with open('/etc/security/pwquality.conf', 'r') as file:
            content = file.read().lower()
        
        if 'minlen' in content and 'minclass' in content:
            result['status'] = True
            result['details'] = "Password quality checking is enforced."
            logger.info(result['details'])
        else:
            result['details'] = "Password quality checking is not enforced."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking password quality enforcement: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'password_quality_check': check_password_quality_enforced()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
