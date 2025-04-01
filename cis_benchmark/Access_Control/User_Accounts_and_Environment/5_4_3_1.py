import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_nologin_in_shells() -> Dict[str, Any]:
    """
    Ensure 'nologin' is not listed in /etc/shells.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.4.3.1',
        'name': "Ensure 'nologin' is not listed in /etc/shells",
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        with open("/etc/shells", "r") as f:
            shells = f.read().splitlines()

        if "/usr/sbin/nologin" in shells or "/sbin/nologin" in shells:
            result['details'] = "'nologin' is listed in /etc/shells."
            logger.warning(result['details'])
        else:
            result['status'] = True
            result['details'] = "'nologin' is not listed in /etc/shells."
            logger.info(result['details'])

    except Exception as e:
        result['details'] = f"Error checking /etc/shells: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'nologin_in_shells': check_nologin_in_shells()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
