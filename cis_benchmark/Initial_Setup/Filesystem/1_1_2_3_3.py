import subprocess
import logging

logger = logging.getLogger(__name__)

def check_home_nosuid_option() -> dict:
    """
    Check if /home has the nosuid option set
    CIS Benchmark 1.1.2.3.3 - Ensure nosuid option set on /home partition

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.1.2.3.3',
        'name': 'Ensure nosuid option set on /home partition',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        # Use mount to check mount options for /home
        mount_cmd = "mount | grep ' /home '"
        mount_result = subprocess.run(mount_cmd, shell=True, capture_output=True, text=True)

        if "nosuid" in mount_result.stdout:
            result['status'] = True
            result['details'] = 'nosuid option is set on /home'
            logger.info(result['details'])
        else:
            result['details'] = 'nosuid option is NOT set on /home'
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f'Error checking nosuid option on /home: {e}'
        logger.error(result['details'])

    return result

def run():
    return {'home_nosuid_option': check_home_nosuid_option()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
