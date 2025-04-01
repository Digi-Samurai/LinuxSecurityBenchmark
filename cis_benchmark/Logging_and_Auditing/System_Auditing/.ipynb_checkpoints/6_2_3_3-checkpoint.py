import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_sudo_log_file_modifications_collected() -> Dict[str, Any]:
    """
    Ensure events that modify the sudo log file are collected.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.3.3',
        'name': "Ensure events that modify the sudo log file are collected",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if sudo log file modifications are logged
        with open('/etc/audit/audit.rules', 'r') as file:
            config = file.readlines()

        sudo_log_mod_logged = False
        for line in config:
            if "sudo" in line and "audit" in line:
                sudo_log_mod_logged = True

        if sudo_log_mod_logged:
            result['status'] = True
            result['details'] = "Modifications to the sudo log file are collected."
            logger.info(result['details'])
        else:
            result['details'] = "Modifications to the sudo log file are not being collected."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking sudo log file modification logging: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'sudo_log_file_modifications_collected': check_sudo_log_file_modifications_collected()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
