import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_min_password_days() -> Dict[str, Any]:
    """
    Ensure minimum password days is configured.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.4.1.2',
        'name': 'Ensure minimum password days is configured',
        'status': False,
        'severity': 'low',
        'details': ''
    }

    try:
        cmd_output = subprocess.run(
            ["grep", "^PASS_MIN_DAYS", "/etc/login.defs"],
            capture_output=True, text=True
        ).stdout.strip()

        if cmd_output and cmd_output.split()[-1].isdigit():
            min_days = int(cmd_output.split()[-1])
            if 1 <= min_days <= 7:
                result['status'] = True
                result['details'] = f"Minimum password days is set to {min_days}."
                logger.info(result['details'])
            else:
                result['details'] = f"Minimum password days is set to {min_days}, which is outside recommended range."
                logger.warning(result['details'])
        else:
            result['details'] = "PASS_MIN_DAYS not properly configured in /etc/login.defs."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking minimum password days: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'min_password_days': check_min_password_days()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
