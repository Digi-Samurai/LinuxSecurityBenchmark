import logging
import subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_rsyslog_installed() -> Dict[str, Any]:
    """
    Ensure rsyslog is installed.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.1.3.1',
        'name': "Ensure rsyslog is installed",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if rsyslog package is installed
        package_status = subprocess.run(
            ["dpkg", "-l", "rsyslog"],
            capture_output=True,
            text=True
        )
        
        if package_status.returncode == 0:
            result['status'] = True
            result['details'] = "rsyslog is installed."
            logger.info(result['details'])
        else:
            result['details'] = "rsyslog is not installed."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking rsyslog installation: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'rsyslog_installed': check_rsyslog_installed()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
