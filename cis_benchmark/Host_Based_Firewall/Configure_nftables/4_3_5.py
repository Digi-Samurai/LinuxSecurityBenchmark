import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_nftables_base_chains() -> Dict[str, Any]:
    """
    Ensure nftables has base chains in at least one table.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '4.3.5',
        'name': 'Ensure nftables base chains exist',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        nft_list_chains = subprocess.run(
            ["nft", "list", "ruleset"], 
            capture_output=True, 
            text=True
        )

        chains = nft_list_chains.stdout.lower()

        # Check if input, forward, and output chains exist
        base_chains_exist = any(chain in chains for chain in ["chain input", "chain forward", "chain output"])

        if base_chains_exist:
            result['status'] = True
            result['details'] = f"Base chains exist:\n{chains}"
            logger.info(result['details'])
        else:
            result['details'] = "No nftables base chains found."
            logger.warning(result['details'])

    except FileNotFoundError:
        result['details'] = "nftables is not installed."
        logger.error(result['details'])

    except subprocess.CalledProcessError as e:
        result['details'] = f"Error checking nftables base chains: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'nftables_base_chains_exist': check_nftables_base_chains()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
