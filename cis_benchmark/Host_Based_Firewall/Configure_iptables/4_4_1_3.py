import subprocess
import logging

logger = logging.getLogger(__name__)

def check_ufw_with_iptables() -> dict:
    """
    Check if ufw is in use with iptables
    CIS Benchmark 4.4.1.3 - Ensure ufw is not in use with iptables
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '4.4.1.3',
        'name': 'Ensure ufw is not in use with iptables',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check if ufw is installed
        ufw_installed_cmd = "rpm -q ufw || dpkg -s ufw"
        ufw_installed_result = subprocess.run(
            ufw_installed_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if iptables is active
        iptables_active_cmd = "iptables -L"
        iptables_active_result = subprocess.run(
            iptables_active_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if ufw service is active
        ufw_active_cmd = "systemctl is-active ufw || ufw status"
        ufw_active_result = subprocess.run(
            ufw_active_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Determine if both are in use
        ufw_installed = ufw_installed_result.returncode == 0
        iptables_active = iptables_active_result.returncode == 0
        ufw_active = (ufw_active_result.stdout.strip() == "active" or 
                     "Status: active" in ufw_active_result.stdout)
        
        if ufw_installed and iptables_active and ufw_active:
            result['status'] = False
            result['details'] = 'Both ufw and iptables are in use simultaneously'
            logger.warning('Both ufw and iptables are in use simultaneously')
        else:
            result['status'] = True
            result['details'] = 'UFW is not in use with iptables'
            logger.info('UFW is not in use with iptables')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking ufw with iptables: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'ufw_with_iptables': check_ufw_with_iptables()
    }
    
    return results

if __name__ == '__main__':
    # Configure basic logging
    logging.basicConfig(level=logging.INFO)
    
    # Direct execution for testing
    print(run())