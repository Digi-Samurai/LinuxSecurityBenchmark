import subprocess
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def get_open_ports() -> List[int]:
    """Retrieve all open ports on the system."""
    open_ports = []

    try:
        netstat_output = subprocess.run(
            ["ss", "-tuln"],
            capture_output=True,
            text=True
        )

        for line in netstat_output.stdout.split("\n"):
            parts = line.split()
            if len(parts) >= 5 and parts[0] in ["tcp", "udp"]:
                port = parts[4].split(":")[-1]
                if port.isdigit():
                    open_ports.append(int(port))

    except Exception as e:
        logger.error(f"Error retrieving open ports: {e}")

    return list(set(open_ports))

def check_iptables_rules_for_ports() -> Dict[str, Any]:
    """
    Ensure iptables rules exist for all open ports.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '4.4.2.4',
        'name': 'Ensure iptables firewall rules exist for all open ports',
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
        open_ports = get_open_ports()
        missing_ports = [port for port in open_ports if str(port) not in rules_output]

        if not missing_ports:
            result['status'] = True
            result['details'] = "iptables rules exist for all open ports."
            logger.info(result['details'])
        else:
            result['details'] = f"Missing iptables rules for ports: {missing_ports}"
            logger.warning(result['details'])

    except FileNotFoundError:
        result['details'] = "iptables is not installed."
        logger.error(result['details'])

    except subprocess.CalledProcessError as e:
        result['details'] = f"Error checking iptables rules: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'iptables_firewall_rules': check_iptables_rules_for_ports()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
