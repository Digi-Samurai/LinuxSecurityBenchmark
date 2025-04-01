import subprocess
import logging

logger = logging.getLogger(__name__)

def check_var_log_nosuid_option() -> dict:
    """
    Check if /var/log has the nosuid option set
    CIS Benchmark 1.1.2.6.3 - Ensure nosuid option set on /var/log partition

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.1.2.6.3',
        'name': 'Ensure nosuid option set on /var/log partition',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        # Check mount options for /var/log
        mount_cmd = "mount | grep ' /var/log '"
        mount_result = subprocess.run(mount_cmd, shell=True, capture_output=True, text=True)

        if "nosuid" in mount_result.stdout:
            result['status'] = True
            result['details'] = 'nosuid option is set on /var/log'
            logger.info(result['details'])
        else:
            result['details'] = 'nosuid option is NOT set on /var/log'
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f'Error checking nosuid option on /var/log: {e}'
        logger.error(result['details'])

    return result

def run():
    return {'var_log_nosuid_option': check_var_log_nosuid_option()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
