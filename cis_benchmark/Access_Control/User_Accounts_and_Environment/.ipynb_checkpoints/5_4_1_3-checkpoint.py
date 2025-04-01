import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_password_expiration_warning() -> Dict[str, Any]:
    """
    Ensure password expiration warning days is configured.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.4.1.3',
        'name': 'Ensure password expiration warning days is configured',
        'status': False,
        'severity': 'low',
        'details': ''
    }

    try:
        cmd_output = subprocess.run(
            ["grep", "^PASS_WARN_AGE", "/etc/login.defs"],
            capture_output=True, text=True
        ).stdout.strip()

        if cmd_output and cmd_output.split()[-1].isdigit():
            warn_days = int(cmd_output.split()[-1])
            if 7 <= warn_days <= 30:
                result['status'] = True
                result['details'] = f"Password expiration warning is set to {warn_days} days."
                logger.info(result['details'])
            else:
                result['details'] = f"Password expiration warning is set to {warn_days}, which is outside recommended range."
                logger.warning(result['details'])
        else:
            result['details'] = "PASS_WARN_AGE not properly configured in /etc/login.defs."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking password expiration warning: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'password_expiration_warning': check_password_expiration_warning()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
