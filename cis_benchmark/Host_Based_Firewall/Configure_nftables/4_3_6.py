import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_nftables_loopback_traffic() -> Dict[str, Any]:
    """
    Ensure nftables is properly configured for loopback traffic.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '4.3.6',
        'name': 'Ensure nftables loopback traffic is configured',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        nft_list_rules = subprocess.run(
            ["nft", "list", "ruleset"], 
            capture_output=True, 
            text=True
        )

        rules_output = nft_list_rules.stdout.lower()

        # Check for loopback traffic rules
        allow_loopback_in = "iif lo accept" in rules_output
        allow_loopback_out = "oif lo accept" in rules_output
        drop_non_loopback_in = "ip saddr 127.0.0.0/8 drop" in rules_output
        drop_non_loopback_out = "ip daddr 127.0.0.0/8 drop" in rules_output

        # All required rules should be present
        if allow_loopback_in and allow_loopback_out and drop_non_loopback_in and drop_non_loopback_out:
            result['status'] = True
            result['details'] = "nftables loopback traffic is correctly configured."
            logger.info(result['details'])
        else:
            result['details'] = "nftables loopback traffic is NOT correctly configured. Add necessary rules."
            logger.warning(result['details'])

    except FileNotFoundError:
        result['details'] = "nftables is not installed."
        logger.error(result['details'])

    except subprocess.CalledProcessError as e:
        result['details'] = f"Error checking nftables loopback rules: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'nftables_loopback_configured': check_nftables_loopback_traffic()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
