import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_nftables_service_enabled() -> Dict[str, Any]:
    """
    Ensure the nftables service is enabled at startup.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '4.3.9',
        'name': 'Ensure nftables service is enabled',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        service_status = subprocess.run(
            ["systemctl", "is-enabled", "nftables"],
            capture_output=True,
            text=True
        )

        if "enabled" in service_status.stdout.strip():
            result['status'] = True
            result['details'] = "nftables service is enabled at startup."
            logger.info(result['details'])
        else:
            result['details'] = "nftables service is NOT enabled."
            logger.warning(result['details'])

    except FileNotFoundError:
        result['details'] = "Systemd is not installed or nftables service is missing."
        logger.error(result['details'])

    except subprocess.CalledProcessError as e:
        result['details'] = f"Error checking nftables service status: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'nftables_service_enabled': check_nftables_service_enabled()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
