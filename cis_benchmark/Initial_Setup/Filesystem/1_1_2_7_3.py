import subprocess
import logging

logger = logging.getLogger(__name__)

def check_var_log_audit_nosuid_option() -> dict:
    """
    Check if /var/log/audit has the nosuid option set
    CIS Benchmark 1.1.2.7.3 - Ensure nosuid option set on /var/log/audit partition

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.1.2.7.3',
        'name': 'Ensure nosuid option set on /var/log/audit partition',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        # Check mount options for /var/log/audit
        mount_cmd = "mount | grep ' /var/log/audit '"
        mount_result = subprocess.run(mount_cmd, shell=True, capture_output=True, text=True)

        if "nosuid" in mount_result.stdout:
            result['status'] = True
            result['details'] = 'nosuid option is set on /var/log/audit'
            logger.info(result['details'])
        else:
            result['details'] = 'nosuid option is NOT set on /var/log/audit'
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f'Error checking nosuid option on /var/log/audit: {e}'
        logger.error(result['details'])

    return result

def run():
    return {'var_log_audit_nosuid_option': check_var_log_audit_nosuid_option()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
