import logging
import subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_rsyslog_log_file_mode() -> Dict[str, Any]:
    """
    Ensure rsyslog log file creation mode is configured.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.1.3.4',
        'name': "Ensure rsyslog log file creation mode is configured",
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        # Check if the rsyslog log file creation mode is configured
        config_check = subprocess.run(
            ["grep", "createMode", "/etc/rsyslog.conf"],
            capture_output=True,
            text=True
        )
        
        if config_check.returncode == 0:
            result['status'] = True
            result['details'] = "Rsyslog log file creation mode is configured."
            logger.info(result['details'])
        else:
            result['details'] = "Rsyslog log file creation mode is not configured."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking rsyslog log file creation mode: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'rsyslog_log_file_creation_mode': check_rsyslog_log_file_mode()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
