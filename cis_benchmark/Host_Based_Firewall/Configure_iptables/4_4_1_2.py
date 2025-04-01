import subprocess
import logging

logger = logging.getLogger(__name__)

def check_nftables_with_iptables() -> dict:
    """
    Check if nftables is in use with iptables
    CIS Benchmark 4.4.1.2 - Ensure nftables is not in use with iptables
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '4.4.1.2',
        'name': 'Ensure nftables is not in use with iptables',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check if nftables is installed
        nft_installed_cmd = "rpm -q nftables || dpkg -s nftables"
        nft_installed_result = subprocess.run(
            nft_installed_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if iptables is also being used
        iptables_active_cmd = "iptables -L"
        iptables_active_result = subprocess.run(
            iptables_active_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if nftables service is running
        nft_running_cmd = "systemctl is-active nftables"
        nft_running_result = subprocess.run(
            nft_running_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Determine if both are in use
        nft_installed = nft_installed_result.returncode == 0
        iptables_active = iptables_active_result.returncode == 0
        nft_running = nft_running_result.stdout.strip() == "active"
        
        if nft_installed and iptables_active and nft_running:
            result['status'] = False
            result['details'] = 'Both nftables and iptables are in use simultaneously'
            logger.warning('Both nftables and iptables are in use simultaneously')
        else:
            result['status'] = True
            result['details'] = 'Nftables is not in use with iptables'
            logger.info('Nftables is not in use with iptables')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking nftables with iptables: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'nftables_with_iptables': check_nftables_with_iptables()
    }
    
    return results

if __name__ == '__main__':
    # Configure basic logging
    logging.basicConfig(level=logging.INFO)
    
    # Direct execution for testing
    print(run())