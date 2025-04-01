import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_kernel_module_collected() -> Dict[str, Any]:
    """
    Ensure kernel module loading, unloading, and modification is collected.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.3.19',
        'name': "Ensure kernel module loading, unloading, and modification is collected",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if kernel module events are logged
        with open('/etc/audit/audit.rules', 'r') as file:
            config = file.readlines()

        kernel_module_logged = False
        for line in config:
            if "modprobe" in line or "insmod" in line or "rmmod" in line:
                kernel_module_logged = True

        if kernel_module_logged:
            result['status'] = True
            result['details'] = "Kernel module loading, unloading, and modification is collected."
            logger.info(result['details'])
        else:
            result['details'] = "Kernel module events are not being collected."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking kernel module logging: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'kernel_module_collected': check_kernel_module_collected()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
