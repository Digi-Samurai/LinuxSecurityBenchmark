import logging
import subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_only_one_logging_system() -> Dict[str, Any]:
    """
    Ensure only one logging system (journald) is in use.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.1.1.4',
        'name': "Ensure only one logging system is in use",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if rsyslog is running (only journald should be active)
        service_status = subprocess.run(
            ["systemctl", "is-active", "rsyslog"],
            capture_output=True,
            text=True
        )
        
        if service_status.stdout.strip() != "active":
            result['status'] = True
            result['details'] = "Only journald is in use for logging."
            logger.info(result['details'])
        else:
            result['details'] = "Both journald and rsyslog are active."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking logging system: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'logging_system_check': check_only_one_logging_system()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
