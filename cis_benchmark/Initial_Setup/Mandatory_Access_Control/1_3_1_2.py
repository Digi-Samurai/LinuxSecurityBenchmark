import subprocess
import logging

logger = logging.getLogger(__name__)

def check_apparmor_enabled_in_bootloader() -> dict:
    """
    Check if AppArmor is enabled in the bootloader configuration.
    CIS Benchmark 1.3.1.2 - Ensure AppArmor is enabled in the bootloader configuration.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.3.1.2',
        'name': 'Ensure AppArmor is enabled in the bootloader configuration',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        cmd = "grep 'apparmor=1 security=apparmor' /etc/default/grub"
        process = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if process.returncode == 0 and 'apparmor=1' in process.stdout and 'security=apparmor' in process.stdout:
            result['status'] = True
            result['details'] = 'AppArmor is enabled in the bootloader'
            logger.info(result['details'])
        else:
            result['status'] = False
            result['details'] = 'AppArmor is NOT properly enabled in the bootloader'
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f'Error checking AppArmor bootloader config: {e}'
        logger.error(result['details'])

    return result

def run():
    return {'apparmor_bootloader_enabled': check_apparmor_enabled_in_bootloader()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
