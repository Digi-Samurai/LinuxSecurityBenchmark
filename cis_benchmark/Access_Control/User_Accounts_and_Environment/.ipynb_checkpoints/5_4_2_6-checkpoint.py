import logging
import os
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_root_umask() -> Dict[str, Any]:
    """
    Ensure root user umask is correctly configured.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.4.2.6',
        'name': 'Ensure root user umask is configured',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        umask_value = os.popen("umask").read().strip()

        if umask_value in ["027", "077"]:
            result['status'] = True
            result['details'] = f"Root user umask is set to {umask_value}."
            logger.info(result['details'])
        else:
            result['details'] = f"Root user umask is set to {umask_value}, expected 027 or 077."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking root umask: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'root_umask': check_root_umask()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
