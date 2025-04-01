import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_ssh_private_key_permissions() -> Dict[str, Any]:
    """
    Ensure permissions on SSH private host key files are configured correctly.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.1.2',
        'name': 'Ensure permissions on SSH private host key files are configured',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        private_key_files = [
            "/etc/ssh/ssh_host_rsa_key",
            "/etc/ssh/ssh_host_ecdsa_key",
            "/etc/ssh/ssh_host_ed25519_key"
        ]
        
        for key_file in private_key_files:
            if os.path.exists(key_file):
                # Get file permissions
                file_stat = os.stat(key_file)
                permissions = oct(file_stat.st_mode)[-3:]

                # Check for recommended permissions (600)
                if permissions == "600":
                    result['status'] = True
                    result['details'] = f"Permissions on {key_file} are correctly configured."
                    logger.info(result['details'])
                else:
                    result['details'] = f"Permissions on {key_file} are not correct. Found: {permissions}. Expected: 600."
                    logger.warning(result['details'])
            else:
                result['details'] = f"SSH private key file {key_file} does not exist."
                logger.error(result['details'])

    except Exception as e:
        result['details'] = f"Error checking permissions for SSH private keys: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'ssh_private_key_permissions': check_ssh_private_key_permissions()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
