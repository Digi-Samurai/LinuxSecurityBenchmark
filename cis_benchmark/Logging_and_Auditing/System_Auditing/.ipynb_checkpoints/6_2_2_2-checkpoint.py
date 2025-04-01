import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_audit_logs_not_automatically_deleted() -> Dict[str, Any]:
    """
    Ensure audit logs are not automatically deleted.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.2.2',
        'name': "Ensure audit logs are not automatically deleted",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if audit logs are configured to be deleted in /etc/audit/auditd.conf
        with open('/etc/audit/auditd.conf', 'r') as file:
            config = file.readlines()

        delete_logs = None
        for line in config:
            if 'max_log_file_action' in line:
                delete_logs = line.split('=')[1].strip().lower()

        if delete_logs != 'rotate':  # Ensure logs are rotated, not deleted
            result['status'] = True
            result['details'] = "Audit logs are not automatically deleted."
            logger.info(result['details'])
        else:
            result['details'] = "Audit logs are configured to be deleted automatically."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking audit log deletion configuration: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'audit_logs_not_automatically_deleted': check_audit_logs_not_automatically_deleted()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
