import os
import logging

logger = logging.getLogger(__name__)

def check_shells_permissions():
    """
    Ensure permissions on /etc/shells are configured.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '7.1.9',
        'name': "Ensure permissions on /etc/shells are configured",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check permissions for /etc/shells
        shells_permissions = oct(os.stat('/etc/shells').st_mode & 0o777)
        if shells_permissions == '0o644':  # Expected permissions for /etc/shells
            result['status'] = True
            result['details'] = f"Permissions on /etc/shells are correctly set: {shells_permissions}"
            logger.info(result['details'])
        else:
            result['details'] = f"Permissions on /etc/shells are incorrectly set: {shells_permissions}. Expected: 644"
            logger.error(result['details'])
    except Exception as e:
        result['details'] = f"Error checking /etc/shells permissions: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'shells_permissions': check_shells_permissions()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
