import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_inactive_password_lock() -> Dict[str, Any]:
    """
    Ensure inactive password lock is configured.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.4.1.5',
        'name': 'Ensure inactive password lock is configured',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        cmd_output = subprocess.run(
            ["useradd", "-D"],
            capture_output=True, text=True
        ).stdout

        for line in cmd_output.splitlines():
            if "INACTIVE=" in line:
                inactive_days = int(line.split("=")[-1].strip())
                if 1 <= inactive_days <= 30:  # Recommended range
                    result['status'] = True
                    result['details'] = f"Inactive password lock is set to {inactive_days} days."
                    logger.info(result['details'])
                else:
                    result['details'] = f"Inactive password lock is set to {inactive_days} days, which is outside recommended range."
                    logger.warning(result['details'])
                break
        else:
            result['details'] = "INACTIVE setting not found in useradd defaults."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking inactive password lock: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'inactive_password_lock': check_inactive_password_lock()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
