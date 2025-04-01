import logging
import subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_journal_remote_service_not_in_use() -> Dict[str, Any]:
    """
    Ensure systemd-journal-remote service is not in use.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.1.2.1.4',
        'name': "Ensure systemd-journal-remote service is not in use",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if systemd-journal-remote service is active
        service_status = subprocess.run(
            ["systemctl", "is-active", "systemd-journal-remote"],
            capture_output=True,
            text=True
        )
        
        if service_status.stdout.strip() == "inactive":
            result['status'] = True
            result['details'] = "systemd-journal-remote service is not in use."
            logger.info(result['details'])
        else:
            result['details'] = "systemd-journal-remote service is in use."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking systemd-journal-remote service: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'journal_remote_service_not_in_use': check_journal_remote_service_not_in_use()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
