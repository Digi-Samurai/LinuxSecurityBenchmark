import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_audit_log_storage_size() -> Dict[str, Any]:
    """
    Ensure audit log storage size is configured.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.2.1',
        'name': "Ensure audit log storage size is configured",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if log file size is set in /etc/audit/auditd.conf
        with open('/etc/audit/auditd.conf', 'r') as file:
            config = file.readlines()

        max_log_file_size = None
        for line in config:
            if 'max_log_file' in line:
                max_log_file_size = int(line.split('=')[1].strip())

        if max_log_file_size and max_log_file_size >= 100:  # 100MB is the recommended size
            result['status'] = True
            result['details'] = "Audit log storage size is configured properly."
            logger.info(result['details'])
        else:
            result['details'] = "Audit log storage size is not configured properly."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking audit log storage size: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'audit_log_storage_size': check_audit_log_storage_size()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
