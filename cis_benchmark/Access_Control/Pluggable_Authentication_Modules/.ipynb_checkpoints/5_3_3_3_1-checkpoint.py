import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_password_history_remember() -> Dict[str, Any]:
    """
    Ensure password history remember is configured.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.3.3.3.1',
        'name': 'Ensure password history remember is configured',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        with open('/etc/security/pwhistory.conf', 'r') as file:
            content = file.read().lower()

        if 'remember' in content:
            result['status'] = True
            result['details'] = "Password history remember is configured."
            logger.info(result['details'])
        else:
            result['details'] = "Password history remember is not configured."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking password history remember setting: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'password_history_remember': check_password_history_remember()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
