import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_sshd_gssapi_authentication_configuration() -> Dict[str, Any]:
    """
    Ensure sshd GSSAPIAuthentication is disabled.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.1.9',
        'name': 'Ensure sshd GSSAPIAuthentication is disabled',
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

        # Check for GSSAPIAuthentication directive
        with open(sshd_config_path, "r") as f:
            sshd_config = f.read().lower()

        if "gssapiauthentication no" in sshd_config:
            result['status'] = True
            result['details'] = "sshd GSSAPIAuthentication is disabled."
            logger.info(result['details'])
        else:
            result['details'] = "sshd GSSAPIAuthentication is not disabled."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking sshd GSSAPIAuthentication configuration: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'sshd_gssapi_authentication_configuration': check_sshd_gssapi_authentication_configuration()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
