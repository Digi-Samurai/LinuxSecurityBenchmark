import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_successful_mounts_collection() -> Dict[str, Any]:
    """
    Ensure successful file system mounts are collected.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.3.10',
        'name': "Ensure successful file system mounts are collected",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check audit rules to collect successful file system mount events
        command = "auditctl -l"
        audit_rules = subprocess.check_output(command, shell=True, text=True)

        # Look for rule related to file system mounts in the audit rules
        if "mount" in audit_rules:
            result['status'] = True
            result['details'] = "Audit rule to collect successful file system mounts is present."
            logger.info(result['details'])
        else:
            result['details'] = "Audit rule to collect successful file system mounts is missing."
            logger.warning(result['details'])

    except subprocess.CalledProcessError as e:
        result['details'] = f"Error checking audit rules: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'successful_filesystem_mounts': check_successful_mounts_collection()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
