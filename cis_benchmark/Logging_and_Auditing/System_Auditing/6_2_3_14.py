import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_mandatory_access_control_modifications_collected() -> Dict[str, Any]:
    """
    Ensure events that modify the system's Mandatory Access Controls are collected.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.3.14',
        'name': "Ensure events that modify the system's Mandatory Access Controls are collected",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if MAC modifications are logged
        with open('/etc/audit/audit.rules', 'r') as file:
            config = file.readlines()

        mac_modifications_logged = False
        for line in config:
            if "mac" in line or "selinux" in line:
                mac_modifications_logged = True

        if mac_modifications_logged:
            result['status'] = True
            result['details'] = "MAC modifications are collected."
            logger.info(result['details'])
        else:
            result['details'] = "MAC modifications are not being collected."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking MAC modification logging: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'mac_modifications_collected': check_mandatory_access_control_modifications_collected()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
