import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_audit_log_files_owner() -> Dict[str, Any]:
    """
    Ensure audit log files owner is configured.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.4.2',
        'name': "Ensure audit log files owner is configured",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        audit_log_files = ['/var/log/audit/audit.log', '/var/log/audit/audit.log.1']  # Modify as needed
        correct_owner = 'root'

        for file in audit_log_files:
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
        result['details'] = f"Error checking audit log files owner: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'audit_log_files_owner': check_audit_log_files_owner()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
