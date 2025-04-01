import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_date_and_time_modifications_collected() -> Dict[str, Any]:
    """
    Ensure events that modify date and time information are collected.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.3.4',
        'name': "Ensure events that modify date and time information are collected",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if modifications to date and time information are logged
        with open('/etc/audit/audit.rules', 'r') as file:
            config = file.readlines()

        date_time_mod_logged = False
        for line in config:
            if "date" in line or "time" in line:
                date_time_mod_logged = True

        if date_time_mod_logged:
            result['status'] = True
            result['details'] = "Modifications to date and time information are collected."
            logger.info(result['details'])
        else:
            result['details'] = "Modifications to date and time information are not being collected."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking date and time modification logging: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'date_and_time_modifications_collected': check_date_and_time_modifications_collected()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
