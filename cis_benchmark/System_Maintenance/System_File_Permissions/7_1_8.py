import os
import logging

logger = logging.getLogger(__name__)

def check_gshadow_dash_permissions():
    """
    Ensure permissions on /etc/gshadow- are configured.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '7.1.8',
        'name': "Ensure permissions on /etc/gshadow- are configured",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check permissions for /etc/gshadow-
        gshadow_dash_permissions = oct(os.stat('/etc/gshadow-').st_mode & 0o777)
        if gshadow_dash_permissions == '0o000':  # Standard permissions for /etc/gshadow-
            result['status'] = True
            result['details'] = f"Permissions on /etc/gshadow- are correctly set: {gshadow_dash_permissions}"
            logger.info(result['details'])
        else:
            result['details'] = f"Permissions on /etc/gshadow- are incorrectly set: {gshadow_dash_permissions}. Expected: 000"
            logger.error(result['details'])
    except Exception as e:
        result['details'] = f"Error checking /etc/gshadow- permissions: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'gshadow_dash_permissions': check_gshadow_dash_permissions()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
