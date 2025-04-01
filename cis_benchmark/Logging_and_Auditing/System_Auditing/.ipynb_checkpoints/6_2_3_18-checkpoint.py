import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_usermod_usage_collected() -> Dict[str, Any]:
    """
    Ensure successful and unsuccessful attempts to use the usermod command are collected.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.3.18',
        'name': "Ensure successful and unsuccessful attempts to use the usermod command are collected",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if usermod command usage is logged
        with open('/etc/audit/audit.rules', 'r') as file:
            config = file.readlines()

        usermod_usage_logged = False
        for line in config:
            if "usermod" in line:
                usermod_usage_logged = True

        if usermod_usage_logged:
            result['status'] = True
            result['details'] = "Successful and unsuccessful attempts to use usermod are collected."
            logger.info(result['details'])
        else:
            result['details'] = "Attempts to use usermod are not being collected."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking usermod logging: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'usermod_usage_collected': check_usermod_usage_collected()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
