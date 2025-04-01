import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_sudo_timeout() -> Dict[str, Any]:
    """
    Ensure sudo authentication timeout is configured correctly.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.2.6',
        'name': 'Ensure sudo authentication timeout is configured correctly',
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

        # Check for sudo timeout setting
        with open(sudo_config_path, "r") as f:
            sudo_config = f.read().lower()

        if "timestamp_timeout" in sudo_config:
            result['status'] = True
            result['details'] = "Sudo authentication timeout is configured correctly."
            logger.info(result['details'])
        else:
            result['details'] = "Sudo authentication timeout is not configured correctly."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking sudo timeout configuration: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'sudo_timeout': check_sudo_timeout()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
