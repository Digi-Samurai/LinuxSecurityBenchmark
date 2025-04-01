import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_system_warns_when_audit_logs_low_space() -> Dict[str, Any]:
    """
    Ensure system warns when audit logs are low on space.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.2.4',
        'name': "Ensure system warns when audit logs are low on space",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if system is configured to warn when audit logs are low on space in /etc/audit/auditd.conf
        with open('/etc/audit/auditd.conf', 'r') as file:
            config = file.readlines()

        space_warn = None
        for line in config:
            if 'space_left_action' in line:
                space_warn = line.split('=')[1].strip()

        if space_warn == 'email':
            result['status'] = True
            result['details'] = "System is configured to warn when audit logs are low on space."
            logger.info(result['details'])
        else:
            result['details'] = "System is not configured to warn when audit logs are low on space."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking audit log space warning configuration: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'system_warns_when_logs_low_space': check_system_warns_when_audit_logs_low_space()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
