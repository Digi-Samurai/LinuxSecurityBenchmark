import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_password_expiration() -> Dict[str, Any]:
    """
    Ensure password expiration is configured.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.4.1.1',
        'name': 'Ensure password expiration is configured',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        cmd_output = subprocess.run(
            ["grep", "^PASS_MAX_DAYS", "/etc/login.defs"],
            capture_output=True, text=True
        ).stdout.strip()

        if cmd_output and cmd_output.split()[-1].isdigit():
            max_days = int(cmd_output.split()[-1])
            if 1 <= max_days <= 365:
                result['status'] = True
                result['details'] = f"Password expiration is set to {max_days} days."
                logger.info(result['details'])
            else:
                result['details'] = f"Password expiration is set to {max_days} days, which is outside recommended range."
                logger.warning(result['details'])
        else:
            result['details'] = "PASS_MAX_DAYS not properly configured in /etc/login.defs."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking password expiration: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'password_expiration': check_password_expiration()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
