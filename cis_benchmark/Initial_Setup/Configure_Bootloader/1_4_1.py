import os
import subprocess
import logging

logger = logging.getLogger(__name__)

def check_bootloader_password() -> dict:
    """
    Ensure bootloader password is set.
    CIS Benchmark 1.4.1 - Ensure bootloader password is set.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.4.1',
        'name': 'Ensure bootloader password is set',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    grub_cfg_path = "/boot/grub/grub.cfg"

    try:
        if os.path.exists(grub_cfg_path):
            cmd = f"grep 'set superusers' {grub_cfg_path}"
            process = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            if process.returncode == 0 and "password_pbkdf2" in process.stdout:
                result['status'] = True
                result['details'] = 'Bootloader password is set'
                logger.info(result['details'])
            else:
                result['status'] = False
                result['details'] = 'Bootloader password is NOT set'
                logger.warning(result['details'])
        else:
            result['status'] = False
            result['details'] = f'Bootloader configuration file {grub_cfg_path} not found'
            logger.error(result['details'])

    except Exception as e:
        result['details'] = f'Error checking bootloader password: {e}'
        logger.error(result['details'])

    return result

def run():
    return {'bootloader_password_set': check_bootloader_password()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
