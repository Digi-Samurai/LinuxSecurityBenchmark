import logging
import subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_rsyslog_service_active() -> Dict[str, Any]:
    """
    Ensure rsyslog service is enabled and active.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.1.3.2',
        'name': "Ensure rsyslog service is enabled and active",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if rsyslog service is active
        service_status = subprocess.run(
            ["systemctl", "is-active", "rsyslog"],
            capture_output=True,
            text=True
        )
        
        if service_status.stdout.strip() == "active":
            result['status'] = True
            result['details'] = "rsyslog service is enabled and active."
            logger.info(result['details'])
        else:
            result['details'] = "rsyslog service is not active."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking rsyslog service: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'rsyslog_service_active': check_rsyslog_service_active()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
