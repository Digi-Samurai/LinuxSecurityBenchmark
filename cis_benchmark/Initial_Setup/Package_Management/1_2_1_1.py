import subprocess
import logging

logger = logging.getLogger(__name__)

def check_gpg_keys() -> dict:
    """
    Check if GPG keys are configured
    CIS Benchmark 1.2.1.1 - Ensure GPG keys are configured (Manual Check)

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.2.1.1',
        'name': 'Ensure GPG keys are configured',
        'status': False,
        'severity': 'high',
        'details': 'This check must be verified manually.'
    }

    try:
        # Check for GPG keys
        gpg_cmd = "apt-key list 2>/dev/null" if is_debian() else "rpm -q gpg-pubkey"
        gpg_result = subprocess.run(gpg_cmd, shell=True, capture_output=True, text=True)

        if gpg_result.returncode == 0 and gpg_result.stdout.strip():
            result['status'] = True
            result['details'] = 'GPG keys are configured'
            logger.info(result['details'])
        else:
            result['details'] = 'No GPG keys found. This must be manually verified.'
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f'Error checking GPG keys: {e}'
        logger.error(result['details'])

    return result

def is_debian():
    """Detect if the system is Debian-based"""
    try:
        return subprocess.run("which apt", shell=True, capture_output=True).returncode == 0
    except:
        return False

def run():
    return {'gpg_keys_configured': check_gpg_keys()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
