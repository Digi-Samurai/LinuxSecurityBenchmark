import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_file_deletion_collected() -> Dict[str, Any]:
    """
    Ensure file deletion events by users are collected.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.3.13',
        'name': "Ensure file deletion events by users are collected",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if file deletion events are logged
        with open('/etc/audit/audit.rules', 'r') as file:
            config = file.readlines()

        file_deletion_logged = False
        for line in config:
            if "unlink" in line or "remove" in line:
                file_deletion_logged = True

        if file_deletion_logged:
            result['status'] = True
            result['details'] = "File deletion events by users are collected."
            logger.info(result['details'])
        else:
            result['details'] = "File deletion events by users are not being collected."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking file deletion logging: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'file_deletion_collected': check_file_deletion_collected()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
