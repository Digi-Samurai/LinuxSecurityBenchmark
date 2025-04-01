import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_user_group_modifications_collected() -> Dict[str, Any]:
    """
    Ensure events that modify user/group information are collected.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.3.8',
        'name': "Ensure events that modify user/group information are collected",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if user/group modifications are logged
        with open('/etc/audit/audit.rules', 'r') as file:
            config = file.readlines()

        user_group_modifications_logged = False
        for line in config:
            if "useradd" in line or "usermod" in line or "groupadd" in line:
                user_group_modifications_logged = True

        if user_group_modifications_logged:
            result['status'] = True
            result['details'] = "User/group modification events are collected."
            logger.info(result['details'])
        else:
            result['details'] = "User/group modification events are not being collected."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking user/group modification logging: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'user_group_modifications_collected': check_user_group_modifications_collected()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
