import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_sudo_log_file() -> Dict[str, Any]:
    """
    Ensure sudo log file exists.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.2.3',
        'name': 'Ensure sudo log file exists',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        sudo_log_path = "/var/log/sudo.log"

        # Check if the sudo log file exists
        if os.path.exists(sudo_log_path):
            result['status'] = True
            result['details'] = f"{sudo_log_path} exists."
            logger.info(result['details'])
        else:
            result['details'] = f"{sudo_log_path} does not exist."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking sudo log file: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'sudo_log_file': check_sudo_log_file()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
