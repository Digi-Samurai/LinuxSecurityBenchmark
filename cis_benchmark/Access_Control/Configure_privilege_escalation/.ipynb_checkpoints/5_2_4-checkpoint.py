import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_sudo_password_required() -> Dict[str, Any]:
    """
    Ensure users must provide password for privilege escalation.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.2.4',
        'name': 'Ensure users must provide password for privilege escalation',
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

        # Check for password required setting in sudoers
        with open(sudo_config_path, "r") as f:
            sudo_config = f.read().lower()

        if "requiretty" in sudo_config or "password" in sudo_config:
            result['status'] = True
            result['details'] = "Users must provide a password for privilege escalation."
            logger.info(result['details'])
        else:
            result['details'] = "Users do not need to provide a password for privilege escalation."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking sudo password requirement: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'sudo_password_required': check_sudo_password_required()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
