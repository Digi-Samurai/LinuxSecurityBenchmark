import subprocess
import logging

logger = logging.getLogger(__name__)

def check_system_updates() -> dict:
    """
    Check if system updates, patches, and security software are installed.
    CIS Benchmark 1.2.2.1 - Ensure updates, patches, and additional security software are installed.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.2.2.1',
        'name': 'Ensure updates, patches, and additional security software are installed',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        if is_debian():
            update_cmd = "apt update && apt list --upgradable"
        elif is_rhel():
            update_cmd = "yum check-update"
        else:
            result['details'] = 'Unsupported OS for this check'
            return result

        update_result = subprocess.run(update_cmd, shell=True, capture_output=True, text=True)

        if update_result.returncode == 0 and update_result.stdout.strip():
            result['status'] = False
            result['details'] = 'Updates are available. Please install them.'
            logger.warning(result['details'])
        else:
            result['status'] = True
            result['details'] = 'All system updates and patches are installed.'
            logger.info(result['details'])

    except Exception as e:
        result['details'] = f'Error checking system updates: {e}'
        logger.error(result['details'])

    return result

def is_debian():
    """Detect if the system is Debian-based"""
    try:
        return subprocess.run("which apt", shell=True, capture_output=True).returncode == 0
    except:
        return False

def is_rhel():
    """Detect if the system is RHEL-based"""
    try:
        return subprocess.run("which yum", shell=True, capture_output=True).returncode == 0
    except:
        return False

def run():
    return {'system_updates_installed': check_system_updates()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
