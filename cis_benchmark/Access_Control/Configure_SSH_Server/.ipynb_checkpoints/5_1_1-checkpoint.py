import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_sshd_config_permissions() -> Dict[str, Any]:
    """
    Ensure permissions on /etc/ssh/sshd_config are configured correctly.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.1.1',
        'name': 'Ensure permissions on /etc/ssh/sshd_config are configured',
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

        # Get file permissions
        file_stat = os.stat(sshd_config_path)
        permissions = oct(file_stat.st_mode)[-3:]

        # Check for recommended permissions (644)
        if permissions == "644":
            result['status'] = True
            result['details'] = f"Permissions on {sshd_config_path} are correctly configured."
            logger.info(result['details'])
        else:
            result['details'] = f"Permissions on {sshd_config_path} are not correct. Found: {permissions}. Expected: 644."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking permissions for {sshd_config_path}: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'sshd_config_permissions': check_sshd_config_permissions()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
