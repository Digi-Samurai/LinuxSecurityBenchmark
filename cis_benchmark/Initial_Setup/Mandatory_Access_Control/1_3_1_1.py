import subprocess
import logging

logger = logging.getLogger(__name__)

def check_apparmor_installed() -> dict:
    """
    Check if AppArmor is installed.
    CIS Benchmark 1.3.1.1 - Ensure AppArmor is installed.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.3.1.1',
        'name': 'Ensure AppArmor is installed',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        cmd = "dpkg -l | grep apparmor"
        process = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if process.returncode == 0 and "apparmor" in process.stdout:
            result['status'] = True
            result['details'] = 'AppArmor is installed'
            logger.info(result['details'])
        else:
            result['status'] = False
            result['details'] = 'AppArmor is NOT installed'
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f'Error checking AppArmor installation: {e}'
        logger.error(result['details'])

    return result

def run():
    return {'apparmor_installed': check_apparmor_installed()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
