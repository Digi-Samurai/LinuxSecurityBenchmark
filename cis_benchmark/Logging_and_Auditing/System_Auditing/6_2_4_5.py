import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_audit_configuration_files_mode() -> Dict[str, Any]:
    """
    Ensure audit configuration files mode is configured.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.4.5',
        'name': "Ensure audit configuration files mode is configured",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    # Define the audit configuration files
    audit_config_files = [
        '/etc/audit/auditd.conf',
        '/etc/audit/rules.d/*.rules',
        '/etc/audit/audit.rules',
        '/etc/audit/audit.conf'
    ]

    try:
        for file_path in audit_config_files:
            # Check if the file exists
            if os.path.exists(file_path):
                # Get the file permissions
                file_mode = oct(os.stat(file_path).st_mode)[-4:]
                if file_mode != '0600':  # We expect the file mode to be 0600
                    result['details'] = f"File {file_path} has incorrect permissions. Expected 0600, found {file_mode}."
                    logger.warning(result['details'])
                    break
                else:
                    result['status'] = True
                    result['details'] = f"File {file_path} has the correct permissions (0600)."
                    logger.info(result['details'])
            else:
                result['details'] = f"Audit configuration file {file_path} does not exist."
                logger.error(result['details'])
                break
    except Exception as e:
        result['details'] = f"Error checking audit configuration file permissions: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'audit_configuration_files_mode': check_audit_configuration_files_mode()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
