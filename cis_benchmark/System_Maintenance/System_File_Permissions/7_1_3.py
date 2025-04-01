import os
import logging

logger = logging.getLogger(__name__)

def check_group_permissions():
    """
    Ensure permissions on /etc/group are configured.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '7.1.3',
        'name': "Ensure permissions on /etc/group are configured",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check permissions for /etc/group
        group_permissions = oct(os.stat('/etc/group').st_mode & 0o777)
        if group_permissions == '0o644':  # Standard permissions for /etc/group
            result['status'] = True
            result['details'] = f"Permissions on /etc/group are correctly set: {group_permissions}"
            logger.info(result['details'])
        else:
            result['details'] = f"Permissions on /etc/group are incorrectly set: {group_permissions}. Expected: 644"
            logger.error(result['details'])
    except Exception as e:
        result['details'] = f"Error checking /etc/group permissions: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'group_permissions': check_group_permissions()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
