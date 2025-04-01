import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_audit_log_file_directory_mode() -> Dict[str, Any]:
    """
    Ensure the audit log file directory mode is configured.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.4.4',
        'name': "Ensure the audit log file directory mode is configured",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        audit_log_dir = '/var/log/audit'
        correct_mode = 0o0750

        if os.path.isdir(audit_log_dir):
            dir_mode = oct(os.stat(audit_log_dir).st_mode & 0o777)
            if dir_mode == oct(correct_mode):
                result['status'] = True
                result['details'] = f"Directory {audit_log_dir} has correct mode: {dir_mode}."
                logger.info(result['details'])
            else:
                result['details'] = f"Directory {audit_log_dir} does not have the correct mode: {dir_mode}."
                logger.warning(result['details'])
        else:
            result['details'] = f"{audit_log_dir} directory does not exist."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking audit log file directory mode: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'audit_log_file_directory_mode': check_audit_log_file_directory_mode()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
