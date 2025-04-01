import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_audit_configuration_files_owner() -> Dict[str, Any]:
    """
    Ensure audit configuration files owner is configured.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.4.6',
        'name': "Ensure audit configuration files owner is configured",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        config_files = ['/etc/audit/audit.rules', '/etc/audit/rules.d']  # Modify as needed
        correct_owner = 'root'

        for file in config_files:
            if os.path.exists(file):
                file_owner = os.stat(file).st_uid
                owner_name = os.getpwuid(file_owner).pw_name
                if owner_name == correct_owner:
                    result['status'] = True
                    result['details'] = f"{file} has the correct owner: {owner_name}."
                    logger.info(result['details'])
                else:
                    result['details'] = f"{file} does not have the correct owner: {owner_name}."
                    logger.warning(result['details'])
            else:
                result['details'] = f"{file} does not exist."
                logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking audit configuration files owner: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'audit_configuration_files_owner': check_audit_configuration_files_owner()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
