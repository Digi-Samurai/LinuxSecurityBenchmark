import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_sudo_use_pty() -> Dict[str, Any]:
    """
    Ensure sudo commands use pty.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.2.2',
        'name': 'Ensure sudo commands use pty',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        sudo_config_path = "/etc/sudoers"

        # Check if the sudoers file exists
        if not os.path.exists(sudo_config_path):
            result['details'] = f"{sudo_config_path} does not exist."
            logger.error(result['details'])
            return result

        # Check for 'use_pty' option in sudoers
        with open(sudo_config_path, "r") as f:
            sudo_config = f.read().lower()

        if "use_pty" in sudo_config:
            result['status'] = True
            result['details'] = "sudo commands use pty."
            logger.info(result['details'])
        else:
            result['details'] = "sudo commands do not use pty."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking sudo pty configuration: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'sudo_use_pty': check_sudo_use_pty()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
