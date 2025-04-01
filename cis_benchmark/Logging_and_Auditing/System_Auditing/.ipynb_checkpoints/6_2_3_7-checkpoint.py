import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_unsuccessful_file_access_collected() -> Dict[str, Any]:
    """
    Ensure unsuccessful file access attempts are collected.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.3.7',
        'name': "Ensure unsuccessful file access attempts are collected",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if unsuccessful file access attempts are logged
        with open('/etc/audit/audit.rules', 'r') as file:
            config = file.readlines()

        unsuccessful_file_access_logged = False
        for line in config:
            if "access" in line and "failure" in line:
                unsuccessful_file_access_logged = True

        if unsuccessful_file_access_logged:
            result['status'] = True
            result['details'] = "Unsuccessful file access attempts are collected."
            logger.info(result['details'])
        else:
            result['details'] = "Unsuccessful file access attempts are not being collected."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking unsuccessful file access logging: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'unsuccessful_file_access_collected': check_unsuccessful_file_access_collected()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
