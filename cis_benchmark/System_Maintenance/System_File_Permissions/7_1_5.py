import os
import logging

logger = logging.getLogger(__name__)

def check_shadow_permissions():
    """
    Ensure permissions on /etc/shadow are configured.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '7.1.5',
        'name': "Ensure permissions on /etc/shadow are configured",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check permissions for /etc/shadow
        shadow_permissions = oct(os.stat('/etc/shadow').st_mode & 0o777)
        if shadow_permissions == '0o000':  # Standard permissions for /etc/shadow
            result['status'] = True
            result['details'] = f"Permissions on /etc/shadow are correctly set: {shadow_permissions}"
            logger.info(result['details'])
        else:
            result['details'] = f"Permissions on /etc/shadow are incorrectly set: {shadow_permissions}. Expected: 000"
            logger.error(result['details'])
    except Exception as e:
        result['details'] = f"Error checking /etc/shadow permissions: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'shadow_permissions': check_shadow_permissions()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
