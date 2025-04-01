import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_actions_as_another_user_logged() -> Dict[str, Any]:
    """
    Ensure actions as another user are always logged.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.3.2',
        'name': "Ensure actions as another user are always logged",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if user switching actions (su/sudo) are logged in /etc/audit/audit.rules
        with open('/etc/audit/audit.rules', 'r') as file:
            config = file.readlines()

        user_switch_logged = False
        for line in config:
            if "execve" in line or "sudo" in line:
                user_switch_logged = True

        if user_switch_logged:
            result['status'] = True
            result['details'] = "Actions as another user are always logged."
            logger.info(result['details'])
        else:
            result['details'] = "Actions as another user are not logged."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking user switch actions logging: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'actions_as_another_user_logged': check_actions_as_another_user_logged()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
