import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_auditd_installed() -> Dict[str, Any]:
    """
    Ensure auditd packages are installed.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.1.1',
        'name': "Ensure auditd packages are installed",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if auditd package is installed
        package_check = subprocess.run(
            ['rpm', '-q', 'audit'],  # For RedHat-based distros, use dpkg for Ubuntu-based
            capture_output=True,
            text=True
        )

        if package_check.returncode == 0:
            result['status'] = True
            result['details'] = "auditd package is installed."
            logger.info(result['details'])
        else:
            result['details'] = "auditd package is not installed."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking auditd installation: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'auditd_installed': check_auditd_installed()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
