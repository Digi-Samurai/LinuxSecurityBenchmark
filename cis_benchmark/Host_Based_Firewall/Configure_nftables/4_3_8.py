import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_nftables_default_deny_policy() -> Dict[str, Any]:
    """
    Ensure nftables has a default deny policy.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '4.3.8',
        'name': 'Ensure nftables default deny firewall policy',
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

        # Check for default deny policies in input, forward, and output chains
        default_deny_input = "chain input { type filter hook input priority 0; policy drop; }" in rules_output
        default_deny_forward = "chain forward { type filter hook forward priority 0; policy drop; }" in rules_output
        default_deny_output = "chain output { type filter hook output priority 0; policy drop; }" in rules_output

        if default_deny_input and default_deny_forward and default_deny_output:
            result['status'] = True
            result['details'] = "nftables default deny policy is correctly configured."
            logger.info(result['details'])
        else:
            result['details'] = "nftables default deny policy is NOT set correctly. Ensure INPUT, FORWARD, and OUTPUT policies are DROP."
            logger.warning(result['details'])

    except FileNotFoundError:
        result['details'] = "nftables is not installed."
        logger.error(result['details'])

    except subprocess.CalledProcessError as e:
        result['details'] = f"Error checking nftables default policy: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'nftables_default_deny_policy': check_nftables_default_deny_policy()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
