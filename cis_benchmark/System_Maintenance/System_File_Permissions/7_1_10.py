import os
import logging

logger = logging.getLogger(__name__)

def check_opasswd_permissions():
    """
    Ensure permissions on /etc/security/opasswd are configured.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '7.1.10',
        'name': "Ensure permissions on /etc/security/opasswd are configured",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check permissions for /etc/security/opasswd
        opasswd_permissions = oct(os.stat('/etc/security/opasswd').st_mode & 0o777)
        if opasswd_permissions == '0o600':  # Expected permissions for /etc/security/opasswd
            result['status'] = True
            result['details'] = f"Permissions on /etc/security/opasswd are correctly set: {opasswd_permissions}"
            logger.info(result['details'])
        else:
            result['details'] = f"Permissions on /etc/security/opasswd are incorrectly set: {opasswd_permissions}. Expected: 600"
            logger.error(result['details'])
    except Exception as e:
        result['details'] = f"Error checking /etc/security/opasswd permissions: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'opasswd_permissions': check_opasswd_permissions()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
