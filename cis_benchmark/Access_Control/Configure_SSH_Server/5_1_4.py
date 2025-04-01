import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_sshd_access_configuration() -> Dict[str, Any]:
    """
    Ensure sshd access is configured correctly.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.1.4',
        'name': 'Ensure sshd access is configured',
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
            result['details'] = "sshd access is correctly configured (PermitRootLogin set to no)."
            logger.info(result['details'])
        else:
            result['details'] = "sshd access is not configured correctly. PermitRootLogin should be set to no."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking sshd access configuration: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'sshd_access_configuration': check_sshd_access_configuration()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
