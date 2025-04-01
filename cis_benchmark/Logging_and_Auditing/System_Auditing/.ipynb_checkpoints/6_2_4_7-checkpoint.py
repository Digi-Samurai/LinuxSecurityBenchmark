import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_audit_configuration_files_group_owner() -> Dict[str, Any]:
    """
    Ensure audit configuration files group owner is configured.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.4.7',
        'name': "Ensure audit configuration files group owner is configured",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        config_files = ['/etc/audit/audit.rules', '/etc/audit/rules.d']  # Modify as needed
        correct_group = 'root'

        for file in config_files:
            if os.path.exists(file):
                file_group = os.stat(file).st_gid
                group_name = os.getgrgid(file_group).gr_name
                if group_name == correct_group:
                    result['status'] = True
                    result['details'] = f"{file} has the correct group owner: {group_name}."
                    logger.info(result['details'])
                else:
                    result['details'] = f"{file} does not have the correct group owner: {group_name}."
                    logger.warning(result['details'])
            else:
                result['details'] = f"{file} does not exist."
                logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking audit configuration files group owner: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'audit_configuration_files_group_owner': check_audit_configuration_files_group_owner()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
