import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_sudo_reauthentication() -> Dict[str, Any]:
    """
    Ensure re-authentication for privilege escalation is not disabled globally.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.2.5',
        'name': 'Ensure re-authentication for privilege escalation is not disabled globally',
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

        # Check for disabling re-authentication
        with open(sudo_config_path, "r") as f:
            sudo_config = f.read().lower()

        if "timestamp_timeout" in sudo_config:
            result['status'] = True
            result['details'] = "Re-authentication for privilege escalation is not disabled globally."
            logger.info(result['details'])
        else:
            result['details'] = "Re-authentication for privilege escalation is disabled globally."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking sudo re-authentication setting: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'sudo_reauthentication': check_sudo_reauthentication()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
