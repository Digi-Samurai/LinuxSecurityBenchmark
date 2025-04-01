import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_iptables_default_deny_policy() -> Dict[str, Any]:
    """
    Ensure iptables has a default deny policy.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '4.4.2.1',
        'name': 'Ensure iptables default deny firewall policy',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        iptables_policy = subprocess.run(
            ["iptables", "-L", "-n"],
            capture_output=True,
            text=True
        )

        rules_output = iptables_policy.stdout.lower()

        if "chain input (policy drop)" in rules_output and \
           "chain forward (policy drop)" in rules_output and \
           "chain output (policy drop)" in rules_output:
            result['status'] = True
            result['details'] = "iptables default deny policy is correctly configured."
            logger.info(result['details'])
        else:
            result['details'] = "iptables default deny policy is NOT set correctly. Ensure INPUT, FORWARD, and OUTPUT policies are DROP."
            logger.warning(result['details'])

    except FileNotFoundError:
        result['details'] = "iptables is not installed."
        logger.error(result['details'])

    except subprocess.CalledProcessError as e:
        result['details'] = f"Error checking iptables default policy: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'iptables_default_deny_policy': check_iptables_default_deny_policy()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())