import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_network_modifications_collected() -> Dict[str, Any]:
    """
    Ensure events that modify the system's network environment are collected.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.3.5',
        'name': "Ensure events that modify the system's network environment are collected",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if network modifications are logged in /etc/audit/audit.rules
        with open('/etc/audit/audit.rules', 'r') as file:
            config = file.readlines()

        network_mod_logged = False
        for line in config:
            if "network" in line:
                network_mod_logged = True

        if network_mod_logged:
            result['status'] = True
            result['details'] = "Modifications to the network environment are collected."
            logger.info(result['details'])
        else:
            result['details'] = "Modifications to the network environment are not being collected."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking network modification logging: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'network_modifications_collected': check_network_modifications_collected()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
