import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_sshd_permit_root_login_configuration() -> Dict[str, Any]:
    """
    Ensure sshd PermitRootLogin is disabled.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.1.20',
        'name': 'Ensure sshd PermitRootLogin is disabled',
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

        # Check for PermitRootLogin directive
        with open(sshd_config_path, "r") as f:
            sshd_config = f.read().lower()

        if "permitrootlogin no" in sshd_config:
            result['status'] = True
            result['details'] = "sshd PermitRootLogin is disabled."
            logger.info(result['details'])
        else:
            result['details'] = "sshd PermitRootLogin is not disabled."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking sshd PermitRootLogin configuration: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'sshd_permit_root_login_configuration': check_sshd_permit_root_login_configuration()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
