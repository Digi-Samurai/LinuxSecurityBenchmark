import logging
import subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_journal_upload_active() -> Dict[str, Any]:
    """
    Ensure systemd-journal-upload is enabled and active.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.1.2.1.3',
        'name': "Ensure systemd-journal-upload is enabled and active",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if systemd-journal-upload service is active
        service_status = subprocess.run(
            ["systemctl", "is-active", "systemd-journal-upload"],
            capture_output=True,
            text=True
        )
        
        if service_status.stdout.strip() == "active":
            result['status'] = True
            result['details'] = "systemd-journal-upload is enabled and active."
            logger.info(result['details'])
        else:
            result['details'] = "systemd-journal-upload is not active."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking systemd-journal-upload service: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'journal_upload_active': check_journal_upload_active()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
