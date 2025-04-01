import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_su_access_restricted() -> Dict[str, Any]:
    """
    Ensure access to the su command is restricted.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.2.7',
        'name': 'Ensure access to the su command is restricted',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        su_path = "/bin/su"

        # Check if su command exists
        if not os.path.exists(su_path):
            result['details'] = f"{su_path} does not exist."
            logger.error(result['details'])
            return result

        # Check if access is restricted (example: via group membership or permissions)
        permissions = os.stat(su_path).st_mode
        if permissions & 0o777 == 0o500:  # Restricted access
            result['status'] = True
            result['details'] = "Access to su command is restricted."
            logger.info(result['details'])
        else:
            result['details'] = "Access to su command is not restricted."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking su command access: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'su_access_restricted': check_su_access_restricted()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
