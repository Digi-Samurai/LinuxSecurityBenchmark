import subprocess
import logging

logger = logging.getLogger(__name__)

def check_apparmor_profiles_enforcing() -> dict:
    """
    Ensure all AppArmor profiles are enforcing.
    CIS Benchmark 1.3.1.4 - Ensure all AppArmor Profiles are enforcing.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.3.1.4',
        'name': 'Ensure all AppArmor Profiles are enforcing',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        cmd = "aa-status --json"
        process = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if process.returncode == 0 and 'complain' not in process.stdout:
            result['status'] = True
            result['details'] = 'All AppArmor profiles are enforcing'
            logger.info(result['details'])
        else:
            result['status'] = False
            result['details'] = 'Some AppArmor profiles are not enforcing'
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f'Error checking AppArmor enforcement: {e}'
        logger.error(result['details'])

    return result

def run():
    return {'apparmor_profiles_enforcing': check_apparmor_profiles_enforcing()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
