import os
import logging

logger = logging.getLogger(__name__)

ISSUE_NET_PATH = "/etc/issue.net"

def check_remote_login_banner() -> dict:
    """
    Ensure remote login warning banner is configured properly.
    CIS Benchmark 1.6.3 - Ensure /etc/issue.net contains a warning message.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.6.3',
        'name': 'Ensure remote login warning banner is configured properly',
        'status': False,
        'severity': 'low',
        'details': ''
    }

    try:
        if os.path.exists(ISSUE_NET_PATH):
            with open(ISSUE_NET_PATH, 'r') as f:
                content = f.read()
            
            if "unauthorized" in content.lower() or "access" in content.lower():
                result['status'] = True
                result['details'] = "Remote login banner is properly configured."
                logger.info(result['details'])
            else:
                result['details'] = "Remote login banner does not contain a proper warning."
                logger.warning(result['details'])
        else:
            result['details'] = "Remote login banner file does not exist."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking remote login banner: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'remote_login_banner': check_remote_login_banner()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
