import subprocess
import logging

logger = logging.getLogger(__name__)

def check_var_nodev_option() -> dict:
    """
    Check if /var has the nodev option set
    CIS Benchmark 1.1.2.4.2 - Ensure nodev option set on /var partition

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.1.2.4.2',
        'name': 'Ensure nodev option set on /var partition',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        # Use mount to check mount options for /var
        mount_cmd = "mount | grep ' /var '"
        mount_result = subprocess.run(mount_cmd, shell=True, capture_output=True, text=True)

        if "nodev" in mount_result.stdout:
            result['status'] = True
            result['details'] = 'nodev option is set on /var'
            logger.info(result['details'])
        else:
            result['details'] = 'nodev option is NOT set on /var'
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f'Error checking nodev option on /var: {e}'
        logger.error(result['details'])

    return result

def run():
    return {'var_nodev_option': check_var_nodev_option()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
