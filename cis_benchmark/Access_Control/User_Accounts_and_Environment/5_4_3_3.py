import logging
import os
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_default_umask() -> Dict[str, Any]:
    """
    Ensure default user umask is correctly configured.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.4.3.3',
        'name': 'Ensure default user umask is configured',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        umask_value = os.popen("umask").read().strip()

        if umask_value in ["027", "077"]:
            result['status'] = True
            result['details'] = f"Default user umask is set to {umask_value}."
            logger.info(result['details'])
        else:
            result['details'] = f"Default user umask is set to {umask_value}, expected 027 or 077."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking default umask: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'default_umask': check_default_umask()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
