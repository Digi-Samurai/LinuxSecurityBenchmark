import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_nftables_installed() -> Dict[str, Any]:
    """
    Check if nftables is installed.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '4.3.1',
        'name': 'Ensure nftables is installed',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        subprocess.run(["nft", "--version"], capture_output=True, check=True, text=True)
        result['status'] = True
        result['details'] = 'nftables is installed.'
        logger.info(result['details'])
    except FileNotFoundError:
        result['details'] = "nftables is NOT installed."
        logger.error(result['details'])
    except subprocess.CalledProcessError as e:
        result['details'] = f"Error checking nftables: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'nftables_installed': check_nftables_installed()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
