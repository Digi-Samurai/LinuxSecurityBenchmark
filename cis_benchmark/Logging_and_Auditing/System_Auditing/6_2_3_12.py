import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_login_logout_collected() -> Dict[str, Any]:
    """
    Ensure login and logout events are collected.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.3.12',
        'name': "Ensure login and logout events are collected",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if login/logout events are logged
        with open('/etc/audit/audit.rules', 'r') as file:
            config = file.readlines()

        login_logout_logged = False
        for line in config:
            if "login" in line or "logout" in line:
                login_logout_logged = True

        if login_logout_logged:
            result['status'] = True
            result['details'] = "Login/logout events are collected."
            logger.info(result['details'])
        else:
            result['details'] = "Login/logout events are not being collected."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking login/logout logging: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'login_logout_collected': check_login_logout_collected()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
