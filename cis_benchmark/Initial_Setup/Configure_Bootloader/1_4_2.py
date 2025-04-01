import os
import subprocess
import logging

logger = logging.getLogger(__name__)

def check_bootloader_permissions() -> dict:
    """
    Ensure access to bootloader config is restricted.
    CIS Benchmark 1.4.2 - Ensure access to bootloader configuration is restricted.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.4.2',
        'name': 'Ensure access to bootloader config is restricted',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    grub_cfg_path = "/boot/grub/grub.cfg"

    try:
        if os.path.exists(grub_cfg_path):
            cmd = f"stat -c %a {grub_cfg_path}"
            process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            permissions = process.stdout.strip()

            if permissions in ['600', '640']:
                result['status'] = True
                result['details'] = f'Bootloader config has secure permissions: {permissions}'
                logger.info(result['details'])
            else:
                result['status'] = False
                result['details'] = f'Bootloader config permissions are too permissive: {permissions}'
                logger.warning(result['details'])
        else:
            result['status'] = False
            result['details'] = f'Bootloader configuration file {grub_cfg_path} not found'
            logger.error(result['details'])

    except Exception as e:
        result['details'] = f'Error checking bootloader permissions: {e}'
        logger.error(result['details'])

    return result

def run():
    return {'bootloader_permissions_restricted': check_bootloader_permissions()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
