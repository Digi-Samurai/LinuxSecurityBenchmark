import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_ufw_default_policy() -> Dict[str, Any]:
    """
    Check if UFW default policy is set to 'deny' for incoming, outgoing, and routed traffic.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '4.2.7',
        'name': 'Ensure UFW default deny firewall policy',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        ufw_status = subprocess.run(
            ["ufw", "status", "verbose"], capture_output=True, text=True, check=True
        )
        output = ufw_status.stdout.lower()

        # Extract default policy settings
        default_in = "default deny incoming" in output
        default_out = "default deny outgoing" in output
        default_fwd = "default deny routed" in output

        if default_in and default_out and default_fwd:
            result['status'] = True
            result['details'] = 'UFW default deny policy is correctly set for incoming, outgoing, and routed traffic.'
            logger.info(result['details'])
        else:
            missing_policies = []
            if not default_in:
                missing_policies.append("incoming")
            if not default_out:
                missing_policies.append("outgoing")
            if not default_fwd:
                missing_policies.append("routed")

            result['details'] = f'UFW default deny policy is not set for: {", ".join(missing_policies)}'
            logger.warning(result['details'])

    except FileNotFoundError:
        result['details'] = "UFW is not installed."
        logger.error(result['details'])

    except subprocess.CalledProcessError as e:
        result['details'] = f"Error checking UFW policy: {e}"
        logger.error(result['details'])

    return result

def run():
    """
    Run all checks for this benchmark section.
    
    :return: Dictionary of check results
    """
    results = {
        'ufw_default_policy': check_ufw_default_policy()
    }
    return results

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
        datefmt="%m/%d/%Y %I:%M:%S %p"
    )
    
    results = run()
