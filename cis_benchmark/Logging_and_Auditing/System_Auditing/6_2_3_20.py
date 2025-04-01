import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_audit_configuration_immutable() -> Dict[str, Any]:
    """
    Ensure the audit configuration is immutable.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.3.20',
        'name': "Ensure the audit configuration is immutable",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if audit configuration is immutable
        audit_config_file = '/etc/audit/audit.rules'
        immutable_config = subprocess.run(['chattr', '+i', audit_config_file], capture_output=True)

        if immutable_config.returncode == 0:
            result['status'] = True
            result['details'] = "Audit configuration is immutable."
            logger.info(result['details'])
        else:
            result['details'] = "Audit configuration is not immutable."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking audit configuration immutability: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'audit_config_immutable': check_audit_configuration_immutable()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
