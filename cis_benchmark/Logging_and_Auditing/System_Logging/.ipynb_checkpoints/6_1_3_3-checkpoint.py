import logging
import subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_journald_send_logs_to_rsyslog() -> Dict[str, Any]:
    """
    Ensure journald is configured to send logs to rsyslog.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.1.3.3',
        'name': "Ensure journald is configured to send logs to rsyslog",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if ForwardToSyslog is enabled in journald configuration
        config_check = subprocess.run(
            ["grep", "ForwardToSyslog", "/etc/systemd/journald.conf"],
            capture_output=True,
            text=True
        )
        
        if config_check.returncode == 0 and "yes" in config_check.stdout.lower():
            result['status'] = True
            result['details'] = "Journald is configured to send logs to rsyslog."
            logger.info(result['details'])
        else:
            result['details'] = "Journald is not configured to send logs to rsyslog."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking journald configuration for rsyslog: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'journald_send_logs_to_rsyslog': check_journald_send_logs_to_rsyslog()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
