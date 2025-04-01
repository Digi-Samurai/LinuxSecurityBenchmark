import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_nftables_table_exists() -> Dict[str, Any]:
    """
    Ensure at least one nftables table exists.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '4.3.4',
        'name': 'Ensure a nftables table exists',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        nft_list = subprocess.run(["nft", "list", "tables"], capture_output=True, text=True)

        if nft_list.stdout.strip():
            result['status'] = True
            result['details'] = f"nftables tables exist:\n{nft_list.stdout.strip()}"
            logger.info(result['details'])
        else:
            result['details'] = "No nftables tables found."
            logger.warning(result['details'])

    except FileNotFoundError:
        result['details'] = "nftables is not installed."
        logger.error(result['details'])

    except subprocess.CalledProcessError as e:
        result['details'] = f"Error checking nftables tables: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'nftables_table_exists': check_nftables_table_exists()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
