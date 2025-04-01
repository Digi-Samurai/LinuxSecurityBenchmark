import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_sshd_kex_algorithms_configuration() -> Dict[str, Any]:
    """
    Ensure sshd KexAlgorithms is configured.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.1.12',
        'name': 'Ensure sshd KexAlgorithms is configured',
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

        # Check for KexAlgorithms directive
        with open(sshd_config_path, "r") as f:
            sshd_config = f.read().lower()

        if "kexalgorithms" in sshd_config:
            result['status'] = True
            result['details'] = "sshd KexAlgorithms is configured."
            logger.info(result['details'])
        else:
            result['details'] = "sshd KexAlgorithms is not configured."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking sshd KexAlgorithms configuration: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'sshd_kex_algorithms_configuration': check_sshd_kex_algorithms_configuration()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
