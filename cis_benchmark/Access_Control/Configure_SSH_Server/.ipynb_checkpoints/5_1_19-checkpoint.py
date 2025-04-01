import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_sshd_permit_empty_passwords_configuration() -> Dict[str, Any]:
    """
    Ensure sshd PermitEmptyPasswords is disabled.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.1.19',
        'name': 'Ensure sshd PermitEmptyPasswords is disabled',
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

        # Check for PermitEmptyPasswords directive
        with open(sshd_config_path, "r") as f:
            sshd_config = f.read().lower()

        if "permitemptypasswords no" in sshd_config:
            result['status'] = True
            result['details'] = "sshd PermitEmptyPasswords is disabled."
            logger.info(result['details'])
        else:
            result['details'] = "sshd PermitEmptyPasswords is not disabled."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking sshd PermitEmptyPasswords configuration: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'sshd_permit_empty_passwords_configuration': check_sshd_permit_empty_passwords_configuration()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
