import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_ufw_disabled_or_uninstalled() -> Dict[str, Any]:
    """
    Ensure UFW is uninstalled or disabled when using nftables.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '4.3.2',
        'name': 'Ensure UFW is uninstalled or disabled with nftables',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        ufw_status = subprocess.run(["systemctl", "is-active", "ufw"], capture_output=True, text=True)
        
        if "inactive" in ufw_status.stdout.lower():
            result['status'] = True
            result['details'] = "UFW is disabled."
            logger.info(result['details'])
        else:
            result['details'] = "UFW is active. It should be disabled when using nftables."
            logger.warning(result['details'])

    except FileNotFoundError:
        result['status'] = True
        result['details'] = "UFW is not installed."
        logger.info(result['details'])

    except subprocess.CalledProcessError as e:
        result['details'] = f"Error checking UFW status: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'ufw_disabled_or_uninstalled': check_ufw_disabled_or_uninstalled()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
