import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_auditd_service() -> Dict[str, Any]:
    """
    Ensure auditd service is enabled and active.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.1.2',
        'name': "Ensure auditd service is enabled and active",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if auditd service is enabled and active
        service_status = subprocess.run(
            ['systemctl', 'is-active', 'auditd'],
            capture_output=True,
            text=True
        )

        if service_status.stdout.strip() == 'active':
            result['status'] = True
            result['details'] = "auditd service is active."
            logger.info(result['details'])
        else:
            result['details'] = "auditd service is not active."
            logger.warning(result['details'])

        service_enabled = subprocess.run(
            ['systemctl', 'is-enabled', 'auditd'],
            capture_output=True,
            text=True
        )

        if service_enabled.stdout.strip() == 'enabled':
            result['status'] = True
            result['details'] += " auditd service is enabled."
            logger.info("auditd service is enabled.")
        else:
            result['details'] += " auditd service is not enabled."
            logger.warning("auditd service is not enabled.")

    except Exception as e:
        result['details'] = f"Error checking auditd service: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'auditd_service': check_auditd_service()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
