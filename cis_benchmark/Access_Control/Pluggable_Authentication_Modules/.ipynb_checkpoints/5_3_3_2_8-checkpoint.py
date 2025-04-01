import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_root_password_quality() -> Dict[str, Any]:
    """
    Ensure password quality is enforced for the root user.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.3.3.2.8',
        'name': 'Ensure password quality is enforced for the root user',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if pwquality module is applied for the root user
        with open('/etc/security/pwquality.conf', 'r') as file:
            content = file.read().lower()

        with open('/etc/pam.d/common-password', 'r') as pam_file:
            pam_content = pam_file.read().lower()

        if 'minlen' in content and 'minclass' in content and 'pam_pwquality.so' in pam_content:
            result['status'] = True
            result['details'] = "Password quality is enforced for the root user."
            logger.info(result['details'])
        else:
            result['details'] = "Password quality is not enforced for the root user."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking root password quality enforcement: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'root_password_quality_check': check_root_password_quality()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
