import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_system_disabled_when_audit_logs_full() -> Dict[str, Any]:
    """
    Ensure system is disabled when audit logs are full.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.2.3',
        'name': "Ensure system is disabled when audit logs are full",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if the system is configured to disable when audit logs are full in /etc/audit/auditd.conf
        with open('/etc/audit/auditd.conf', 'r') as file:
            config = file.readlines()

        full_log_action = None
        for line in config:
            if 'disk_full_action' in line:
                full_log_action = line.split('=')[1].strip()

        if full_log_action == 'syslog':
            result['status'] = True
            result['details'] = "System is configured to disable when audit logs are full."
            logger.info(result['details'])
        else:
            result['details'] = "System is not configured to disable when audit logs are full."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking audit log full action: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'system_disabled_when_logs_full': check_system_disabled_when_audit_logs_full()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
