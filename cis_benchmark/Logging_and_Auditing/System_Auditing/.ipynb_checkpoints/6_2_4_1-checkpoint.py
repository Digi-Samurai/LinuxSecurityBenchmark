import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_audit_log_files_mode() -> Dict[str, Any]:
    """
    Ensure audit log files mode is configured.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.4.1',
        'name': "Ensure audit log files mode is configured",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        audit_log_files = ['/var/log/audit/audit.log', '/var/log/audit/audit.log.1']  # Modify as needed
        correct_mode = 0o0600

        for file in audit_log_files:
            if os.path.exists(file):
                file_mode = oct(os.stat(file).st_mode & 0o777)
                if file_mode == oct(correct_mode):
                    result['status'] = True
                    result['details'] = f"{file} has correct mode: {file_mode}."
                    logger.info(result['details'])
                else:
                    result['details'] = f"{file} does not have the correct mode: {file_mode}."
                    logger.warning(result['details'])
            else:
                result['details'] = f"{file} does not exist."
                logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking audit log files mode: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'audit_log_files_mode': check_audit_log_files_mode()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
