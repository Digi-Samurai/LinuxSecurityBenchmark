import logging
import subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_forward_to_syslog_disabled() -> Dict[str, Any]:
    """
    Ensure journald ForwardToSyslog is disabled.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.1.2.2',
        'name': "Ensure journald ForwardToSyslog is disabled",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if ForwardToSyslog is set to no
        config_check = subprocess.run(
            ["grep", "ForwardToSyslog", "/etc/systemd/journald.conf"],
            capture_output=True,
            text=True
        )
        
        if config_check.returncode == 0 and "no" in config_check.stdout.lower():
            result['status'] = True
            result['details'] = "ForwardToSyslog is disabled in journald."
            logger.info(result['details'])
        else:
            result['details'] = "ForwardToSyslog is not disabled in journald."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking ForwardToSyslog in journald: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'journald_forward_to_syslog_disabled': check_forward_to_syslog_disabled()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
