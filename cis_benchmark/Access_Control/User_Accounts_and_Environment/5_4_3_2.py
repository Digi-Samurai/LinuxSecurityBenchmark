import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_shell_timeout() -> Dict[str, Any]:
    """
    Ensure the default user shell timeout is configured.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.4.3.2',
        'name': "Ensure default user shell timeout is configured",
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        timeout_vars = ["TMOUT", "readonly TMOUT"]
        timeout_configured = False

        with open("/etc/profile", "r") as f:
            profile_content = f.read()

        with open("/etc/bash.bashrc", "r") as f:
            bashrc_content = f.read()

        for var in timeout_vars:
            if var in profile_content or var in bashrc_content:
                timeout_configured = True
                break

        if timeout_configured:
            result['status'] = True
            result['details'] = "Shell timeout is correctly configured."
            logger.info(result['details'])
        else:
            result['details'] = "Shell timeout is not configured."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking shell timeout: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'shell_timeout': check_shell_timeout()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
