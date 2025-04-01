import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_session_initiation_collected() -> Dict[str, Any]:
    """
    Ensure session initiation information is collected.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.3.11',
        'name': "Ensure session initiation information is collected",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if session initiation is logged
        with open('/etc/audit/audit.rules', 'r') as file:
            config = file.readlines()

        session_initiation_logged = False
        for line in config:
            if "session" in line:
                session_initiation_logged = True

        if session_initiation_logged:
            result['status'] = True
            result['details'] = "Session initiation events are collected."
            logger.info(result['details'])
        else:
            result['details'] = "Session initiation events are not being collected."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking session initiation logging: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'session_initiation_collected': check_session_initiation_collected()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
