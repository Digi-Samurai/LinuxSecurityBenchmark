import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_sshd_log_level_configuration() -> Dict[str, Any]:
    """
    Ensure sshd LogLevel is configured.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.1.14',
        'name': 'Ensure sshd LogLevel is configured',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        sshd_config_path = "/etc/ssh/sshd_config"
        
        # Check if the file exists
        if not os.path.exists(sshd_config_path):
            result['details'] = f"{sshd_config_path} does not exist."
            logger.error(result['details'])
            return result

        # Check for LogLevel directive
        with open(sshd_config_path, "r") as f:
            sshd_config = f.read().lower()

        if "loglevel" in sshd_config:
            result['status'] = True
            result['details'] = "sshd LogLevel is configured."
            logger.info(result['details'])
        else:
            result['details'] = "sshd LogLevel is not configured."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking sshd LogLevel configuration: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'sshd_log_level_configuration': check_sshd_log_level_configuration()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
