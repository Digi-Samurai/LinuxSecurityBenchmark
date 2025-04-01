import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_audit_backlog_limit() -> Dict[str, Any]:
    """
    Ensure audit_backlog_limit is sufficient.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.1.4',
        'name': "Ensure audit_backlog_limit is sufficient",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check audit_backlog_limit value in /etc/audit/auditd.conf
        with open('/etc/audit/auditd.conf', 'r') as file:
            config = file.readlines()
        
        backlog_limit = None
        for line in config:
            if 'audit_backlog_limit' in line:
                backlog_limit = int(line.split('=')[1].strip())

        if backlog_limit and backlog_limit >= 8192:  # 8192 is a recommended value
            result['status'] = True
            result['details'] = "audit_backlog_limit is configured sufficiently."
            logger.info(result['details'])
        else:
            result['details'] = "audit_backlog_limit is insufficient."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking audit_backlog_limit: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'audit_backlog_limit': check_audit_backlog_limit()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
