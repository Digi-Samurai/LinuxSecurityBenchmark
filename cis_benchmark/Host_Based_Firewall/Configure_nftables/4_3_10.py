import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_nftables_rules_persistent() -> Dict[str, Any]:
    """
    Ensure nftables rules are persistent across reboots.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '4.3.10',
        'name': 'Ensure nftables rules are permanent',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        nft_conf_exists = subprocess.run(
            ["test", "-f", "/etc/nftables.conf"],
            capture_output=True
        )

        if nft_conf_exists.returncode == 0:
            result['status'] = True
            result['details'] = "nftables rules are persistent across reboots."
            logger.info(result['details'])
        else:
            result['details'] = "nftables rules are NOT persistent."
            logger.warning(result['details'])

    except FileNotFoundError:
        result['details'] = "nftables is not installed."
        logger.error(result['details'])

    except subprocess.CalledProcessError as e:
        result['details'] = f"Error checking nftables persistence: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'nftables_rules_persistent': check_nftables_rules_persistent()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
