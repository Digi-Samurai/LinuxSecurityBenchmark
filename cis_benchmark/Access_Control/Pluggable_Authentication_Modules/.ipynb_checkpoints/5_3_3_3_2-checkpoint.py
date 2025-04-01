import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_root_password_history() -> Dict[str, Any]:
    """
    Ensure password history is enforced for the root user.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.3.3.3.2',
        'name': 'Ensure password history is enforced for the root user',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        with open('/etc/security/pwhistory.conf', 'r') as file:
            content = file.read().lower()

        if 'remember' in content and 'root' in content:
            result['status'] = True
            result['details'] = "Password history is enforced for the root user."
            logger.info(result['details'])
        else:
            result['details'] = "Password history is not enforced for the root user."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking root password history enforcement: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'root_password_history': check_root_password_history()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
