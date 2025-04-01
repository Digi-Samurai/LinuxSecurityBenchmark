import os
import logging

logger = logging.getLogger(__name__)

ISSUE_PATH = "/etc/issue"

def check_local_login_banner() -> dict:
    """
    Ensure local login warning banner is configured properly.
    CIS Benchmark 1.6.2 - Ensure /etc/issue contains a warning message.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.6.2',
        'name': 'Ensure local login warning banner is configured properly',
        'status': False,
        'severity': 'low',
        'details': ''
    }

    try:
        if os.path.exists(ISSUE_PATH):
            with open(ISSUE_PATH, 'r') as f:
                content = f.read()
            
            if "unauthorized" in content.lower() or "access" in content.lower():
                result['status'] = True
                result['details'] = "Local login banner is properly configured."
                logger.info(result['details'])
            else:
                result['details'] = "Local login banner does not contain a proper warning."
                logger.warning(result['details'])
        else:
            result['details'] = "Local login banner file does not exist."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking local login banner: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'local_login_banner': check_local_login_banner()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
