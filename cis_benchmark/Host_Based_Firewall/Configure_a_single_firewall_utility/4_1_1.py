import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_firewall_utility() -> Dict[str, Any]:
    """
    Check for a single firewall configuration utility
    CIS Benchmark 4.1.1 - Ensure a single firewall configuration utility is in use
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '4.1.1',
        'name': 'Ensure a single firewall configuration utility is in use',
        'status': False,  # False means not compliant
        'severity': 'medium',
        'details': '',
        'installed_firewalls': []
    }
    
    # List of common firewall utilities to check
    firewall_utilities = [
        'ufw',        # Uncomplicated Firewall (Ubuntu)
        'firewalld',  # FirewallD (CentOS, RHEL)
        'iptables',   # Traditional iptables
        'nftables',   # nftables (newer replacement for iptables)
        'ipfw',       # BSD-style firewall
    ]
    
    try:
        # Check which firewall utilities are installed
        installed_firewalls = []
        
        for utility in firewall_utilities:
            try:
                # Check if utility is installed
                subprocess.run(
                    ['which', utility], 
                    check=True, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE
                )
                installed_firewalls.append(utility)
            except subprocess.CalledProcessError:
                # Utility not found, continue checking others
                continue
        
        # Check active firewall status
        active_firewalls = []
        for utility in installed_firewalls:
            try:
                if utility == 'ufw':
                    # Check UFW status
                    ufw_status = subprocess.run(
                        ['ufw', 'status'], 
                        capture_output=True, 
                        text=True
                    )
                    if 'Status: active' in ufw_status.stdout:
                        active_firewalls.append(utility)
                
                elif utility == 'firewalld':
                    # Check FirewallD status
                    firewalld_status = subprocess.run(
                        ['systemctl', 'is-active', 'firewalld'], 
                        capture_output=True, 
                        text=True
                    )
                    if firewalld_status.stdout.strip() == 'active':
                        active_firewalls.append(utility)
                
                elif utility == 'iptables':
                    # Check if iptables has any active rules
                    iptables_status = subprocess.run(
                        ['iptables', '-L'], 
                        capture_output=True, 
                        text=True
                    )
                    if iptables_status.returncode == 0:
                        active_firewalls.append(utility)
                
                elif utility == 'nftables':
                    # Check nftables active ruleset
                    nftables_status = subprocess.run(
                        ['nft', 'list', 'ruleset'], 
                        capture_output=True, 
                        text=True
                    )
                    if nftables_status.returncode == 0:
                        active_firewalls.append(utility)
            
            except Exception as e:
                logger.debug(f"Error checking {utility} status: {e}")
        
        # Update result
        result['installed_firewalls'] = installed_firewalls
        
        # Compliance check: only one firewall should be in use
        if len(active_firewalls) == 1:
            result['status'] = True
            result['details'] = f'Single firewall utility in use: {active_firewalls[0]}'
            logger.info(result['details'])
        elif len(active_firewalls) > 1:
            result['details'] = f'Multiple firewall utilities active: {", ".join(active_firewalls)}'
            logger.warning(result['details'])
        else:
            result['details'] = 'No active firewall utilities found'
            logger.warning(result['details'])
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking firewall utilities: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'firewall_utility': check_firewall_utility()
    }
    
    return results

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Direct execution for testing
    results = run()
    print(results['firewall_utility'])