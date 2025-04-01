import logging
import subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_rsyslog_receive_remote_logs() -> Dict[str, Any]:
    """
    Ensure rsyslog is not configured to receive logs from a remote client.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.1.3.7',
        'name': "Ensure rsyslog is not configured to receive logs from a remote client",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if rsyslog is configured to receive logs from remote clients
        config_check = subprocess.run(
            ["grep", "module(load=\"imudp\")", "/etc/rsyslog.conf"],
            capture_output=True,
            text=True
        )
        
        if config_check.returncode == 0:
            result['details'] = "rsyslog is configured to receive logs from a remote client (UDP)."
            logger.warning(result['details'])
        else:
            # Check for TCP module
            config_check_tcp = subprocess.run(
                ["grep", "module(load=\"imtcp\")", "/etc/rsyslog.conf"],
                capture_output=True,
                text=True
            )
            
            if config_check_tcp.returncode == 0:
                result['details'] = "rsyslog is configured to receive logs from a remote client (TCP)."
                logger.warning(result['details'])
            else:
                result['status'] = True
                result['details'] = "rsyslog is not configured to receive logs from a remote client."
                logger.info(result['details'])

    except Exception as e:
        result['details'] = f"Error checking rsyslog remote log reception: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'rsyslog_receive_remote_logs': check_rsyslog_receive_remote_logs()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
