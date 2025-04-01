import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_auditd_pre_start() -> Dict[str, Any]:
    """
    Ensure auditing for processes that start prior to auditd is enabled.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.1.3',
        'name': "Ensure auditing for processes that start prior to auditd is enabled",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check kernel boot parameters for audit=1
        kernel_params = subprocess.run(
            ['grubby', '--info', '/boot/grub2/grub.cfg'],
            capture_output=True,
            text=True
        )

        if 'audit=1' in kernel_params.stdout:
            result['status'] = True
            result['details'] = "Auditing for processes starting prior to auditd is enabled."
            logger.info(result['details'])
        else:
            result['details'] = "Auditing for processes starting prior to auditd is not enabled."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking auditing for processes starting prior to auditd: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'auditd_pre_start': check_auditd_pre_start()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
