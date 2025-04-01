import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_privileged_commands_collected() -> Dict[str, Any]:
    """
    Ensure use of privileged commands are collected.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.3.6',
        'name': "Ensure use of privileged commands are collected",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if privileged command usage (e.g., sudo) is being logged
        with open('/etc/audit/audit.rules', 'r') as file:
            config = file.readlines()

        privileged_commands_logged = False
        for line in config:
            if "sudo" in line or "execve" in line:
                privileged_commands_logged = True

        if privileged_commands_logged:
            result['status'] = True
            result['details'] = "Use of privileged commands is collected."
            logger.info(result['details'])
        else:
            result['details'] = "Use of privileged commands is not being collected."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking privileged command logging: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'privileged_commands_collected': check_privileged_commands_collected()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
