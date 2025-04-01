import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_iptables_loopback_traffic() -> Dict[str, Any]:
    """
    Ensure iptables loopback traffic is configured correctly.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '4.4.2.2',
        'name': 'Ensure iptables loopback traffic is configured',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        iptables_rules = subprocess.run(
            ["iptables", "-S"],
            capture_output=True,
            text=True
        )

        rules_output = iptables_rules.stdout.lower()

        allow_lo_in = "-A INPUT -i lo -j ACCEPT" in rules_output
        allow_lo_out = "-A OUTPUT -o lo -j ACCEPT" in rules_output
        deny_127_in = "-A INPUT -s 127.0.0.0/8 -j DROP" in rules_output

        if allow_lo_in and allow_lo_out and deny_127_in:
            result['status'] = True
            result['details'] = "iptables loopback traffic is correctly configured."
            logger.info(result['details'])
        else:
            result['details'] = "iptables loopback traffic is NOT correctly configured."
            logger.warning(result['details'])

    except FileNotFoundError:
        result['details'] = "iptables is not installed."
        logger.error(result['details'])

    except subprocess.CalledProcessError as e:
        result['details'] = f"Error checking iptables loopback traffic: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'iptables_loopback_traffic': check_iptables_loopback_traffic()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
