import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_password_hashing_algorithm() -> Dict[str, Any]:
    """
    Ensure strong password hashing algorithm is configured.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.4.1.4',
        'name': 'Ensure strong password hashing algorithm is configured',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        with open('/etc/login.defs', 'r') as file:
            content = file.read()

        if 'ENCRYPT_METHOD SHA512' in content or 'ENCRYPT_METHOD YESCRYPT' in content:
            result['status'] = True
            result['details'] = "Strong password hashing algorithm is configured."
            logger.info(result['details'])
        else:
            result['details'] = "Strong password hashing algorithm is NOT configured."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking password hashing algorithm: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'password_hashing_algorithm': check_password_hashing_algorithm()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
