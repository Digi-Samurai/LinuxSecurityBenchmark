import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_pam_pwhistory_enabled() -> Dict[str, Any]:
    """
    Ensure pam_pwhistory module is enabled.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.3.2.4',
        'name': 'Ensure pam_pwhistory module is enabled',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check for pam_pwhistory in /etc/pam.d/common-password or similar files
        with open('/etc/pam.d/common-password', 'r') as pam_file:
            pam_content = pam_file.read().lower()
        
        if 'pam_pwhistory.so' in pam_content:
            result['status'] = True
            result['details'] = "pam_pwhistory module is enabled."
            logger.info(result['details'])
        else:
            result['details'] = "pam_pwhistory module is not enabled."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking pam_pwhistory module: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'pam_pwhistory_enabled': check_pam_pwhistory_enabled()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
