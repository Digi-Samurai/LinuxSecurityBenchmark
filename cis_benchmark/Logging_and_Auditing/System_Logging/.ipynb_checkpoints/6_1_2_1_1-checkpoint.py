import logging
import subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_journal_remote_installed() -> Dict[str, Any]:
    """
    Ensure systemd-journal-remote is installed.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.1.2.1.1',
        'name': "Ensure systemd-journal-remote is installed",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if systemd-journal-remote package is installed
        package_status = subprocess.run(
            ["dpkg", "-l", "systemd-journal-remote"],
            capture_output=True,
            text=True
        )
        
        if package_status.returncode == 0:
            result['status'] = True
            result['details'] = "systemd-journal-remote is installed."
            logger.info(result['details'])
        else:
            result['details'] = "systemd-journal-remote is not installed."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking systemd-journal-remote installation: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'journal_remote_installed': check_journal_remote_installed()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
