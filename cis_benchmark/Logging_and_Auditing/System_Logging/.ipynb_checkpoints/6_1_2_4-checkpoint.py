import logging
import subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_journald_storage_configured() -> Dict[str, Any]:
    """
    Ensure journald Storage is configured.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.1.2.4',
        'name': "Ensure journald Storage is configured",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if Storage is set in journald.conf
        config_check = subprocess.run(
            ["grep", "Storage", "/etc/systemd/journald.conf"],
            capture_output=True,
            text=True
        )
        
        if config_check.returncode == 0:
            result['status'] = True
            result['details'] = "Journald Storage is configured."
            logger.info(result['details'])
        else:
            result['details'] = "Journald Storage is not configured."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking journald storage: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'journald_storage_configured': check_journald_storage_configured()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
