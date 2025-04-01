import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_changes_to_sudoers_collected() -> Dict[str, Any]:
    """
    Ensure changes to system administration scope (sudoers) are collected.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.3.1',
        'name': "Ensure changes to system administration scope (sudoers) is collected",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if sudoers file changes are being logged
        with open('/etc/audit/audit.rules', 'r') as file:
            config = file.readlines()

        sudoers_logged = False
        for line in config:
            if "sudoers" in line and "audit" in line:
                sudoers_logged = True

        if sudoers_logged:
            result['status'] = True
            result['details'] = "Changes to sudoers file are collected."
            logger.info(result['details'])
        else:
            result['details'] = "Changes to sudoers file are not being collected."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking sudoers file changes logging: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'changes_to_sudoers_collected': check_changes_to_sudoers_collected()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
