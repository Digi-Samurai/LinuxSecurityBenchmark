import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_chacl_usage_collected() -> Dict[str, Any]:
    """
    Ensure successful and unsuccessful attempts to use the chacl command are collected.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.3.17',
        'name': "Ensure successful and unsuccessful attempts to use the chacl command are collected",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if chacl command usage is logged
        with open('/etc/audit/audit.rules', 'r') as file:
            config = file.readlines()

        chacl_usage_logged = False
        for line in config:
            if "chacl" in line:
                chacl_usage_logged = True

        if chacl_usage_logged:
            result['status'] = True
            result['details'] = "Successful and unsuccessful attempts to use chacl are collected."
            logger.info(result['details'])
        else:
            result['details'] = "Attempts to use chacl are not being collected."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking chacl logging: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'chacl_usage_collected': check_chacl_usage_collected()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
