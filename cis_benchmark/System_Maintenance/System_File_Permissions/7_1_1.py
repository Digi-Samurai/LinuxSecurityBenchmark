import os
import logging

logger = logging.getLogger(__name__)

def check_passwd_permissions():
    """
    Ensure permissions on /etc/passwd are configured.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '7.1.1',
        'name': "Ensure permissions on /etc/passwd are configured",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check permissions for /etc/passwd
        passwd_permissions = oct(os.stat('/etc/passwd').st_mode & 0o777)
        if passwd_permissions == '0o644':  # Standard permissions for /etc/passwd
            result['status'] = True
            result['details'] = f"Permissions on /etc/passwd are correctly set: {passwd_permissions}"
            logger.info(result['details'])
        else:
            result['details'] = f"Permissions on /etc/passwd are incorrectly set: {passwd_permissions}. Expected: 644"
            logger.error(result['details'])
    except Exception as e:
        result['details'] = f"Error checking /etc/passwd permissions: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'passwd_permissions': check_passwd_permissions()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
