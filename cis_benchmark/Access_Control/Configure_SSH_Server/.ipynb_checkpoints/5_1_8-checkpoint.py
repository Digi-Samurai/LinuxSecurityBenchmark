import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_sshd_disable_forwarding_configuration() -> Dict[str, Any]:
    """
    Ensure sshd DisableForwarding is enabled.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.1.8',
        'name': 'Ensure sshd DisableForwarding is enabled',
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

        # Check for DisableForwarding directive
        with open(sshd_config_path, "r") as f:
            sshd_config = f.read().lower()

        if "disableforwarding yes" in sshd_config:
            result['status'] = True
            result['details'] = "sshd DisableForwarding is enabled."
            logger.info(result['details'])
        else:
            result['details'] = "sshd DisableForwarding is not enabled."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking sshd DisableForwarding configuration: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'sshd_disable_forwarding_configuration': check_sshd_disable_forwarding_configuration()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
