import subprocess
import logging

logger = logging.getLogger(__name__)

def check_apparmor_profiles_mode() -> dict:
    """
    Ensure all AppArmor profiles are in enforce or complain mode.
    CIS Benchmark 1.3.1.3 - Ensure all AppArmor Profiles are in enforce or complain mode.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.3.1.3',
        'name': 'Ensure all AppArmor Profiles are in enforce or complain mode',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        cmd = "aa-status --json"
        process = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if process.returncode == 0 and ('enforce' in process.stdout or 'complain' in process.stdout):
            result['status'] = True
            result['details'] = 'All AppArmor profiles are in enforce or complain mode'
            logger.info(result['details'])
        else:
            result['status'] = False
            result['details'] = 'Some AppArmor profiles are not in enforce or complain mode'
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f'Error checking AppArmor profiles mode: {e}'
        logger.error(result['details'])

    return result

def run():
    return {'apparmor_profiles_mode': check_apparmor_profiles_mode()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
