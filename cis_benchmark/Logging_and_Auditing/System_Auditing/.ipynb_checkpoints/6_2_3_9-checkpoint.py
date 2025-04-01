import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_dac_permission_modifications_collected() -> Dict[str, Any]:
    """
    Ensure discretionary access control permission modification events are collected.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.3.9',
        'name': "Ensure discretionary access control permission modification events are collected",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if DAC permission modification events are logged
        with open('/etc/audit/audit.rules', 'r') as file:
            config = file.readlines()

        dac_permission_mod_logged = False
        for line in config:
            if "chmod" in line or "chown" in line or "setfacl" in line:
                dac_permission_mod_logged = True

        if dac_permission_mod_logged:
            result['status'] = True
            result['details'] = "DAC permission modification events are collected."
            logger.info(result['details'])
        else:
            result['details'] = "DAC permission modification events are not being collected."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking DAC permission modification logging: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'dac_permission_modifications_collected': check_dac_permission_modifications_collected()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
