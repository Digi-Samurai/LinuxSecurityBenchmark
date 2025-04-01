import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_failed_attempts_lockout_includes_root() -> Dict[str, Any]:
    """
    Ensure password failed attempts lockout includes root account.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.3.3.1.3',
        'name': 'Ensure password failed attempts lockout includes root account',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check for pam_faillock configuration in /etc/pam.d/common-auth or similar files
        with open('/etc/pam.d/common-auth', 'r') as pam_file:
            pam_content = pam_file.read().lower()
        
        if 'pam_faillock.so' in pam_content and 'root' in pam_content:
            result['status'] = True
            result['details'] = "Password failed attempts lockout includes root account."
            logger.info(result['details'])
        else:
            result['details'] = "Password failed attempts lockout does not include root account."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking root account lockout: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'failed_attempts_lockout_includes_root': check_failed_attempts_lockout_includes_root()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
