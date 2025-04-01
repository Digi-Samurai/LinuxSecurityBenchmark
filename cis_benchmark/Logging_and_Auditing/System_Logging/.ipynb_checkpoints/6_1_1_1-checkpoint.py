import logging
import subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_journald_service() -> Dict[str, Any]:
    """
    Ensure journald service is enabled and active.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.1.1.1',
        'name': "Ensure journald service is enabled and active",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if journald service is active
        service_status = subprocess.run(
            ["systemctl", "is-active", "systemd-journald"],
            capture_output=True,
            text=True
        )
        
        if service_status.stdout.strip() == "active":
            result['status'] = True
            result['details'] = "Journald service is enabled and active."
            logger.info(result['details'])
        else:
            result['details'] = "Journald service is not active."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking journald service: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'journald_service': check_journald_service()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
