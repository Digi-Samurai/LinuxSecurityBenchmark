import subprocess
import logging

logger = logging.getLogger(__name__)

def check_iptables_installed() -> dict:
    """
    Check if iptables packages are installed
    CIS Benchmark 4.4.1.1 - Ensure iptables packages are installed
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '4.4.1.1',
        'name': 'Ensure iptables packages are installed',
        'status': False,
        'severity': 'high',
        'details': ''
    }
    
    try:
        # Check if iptables is installed
        iptables_cmd = "rpm -q iptables iptables-services || dpkg -s iptables iptables-persistent"
        iptables_result = subprocess.run(
            iptables_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        if iptables_result.returncode == 0:
            result['status'] = True
            result['details'] = 'Iptables packages are installed'
            logger.info('Iptables packages are installed')
        else:
            result['status'] = False
            result['details'] = 'Iptables packages are not installed'
            logger.warning('Iptables packages are not installed')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking iptables installation: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'iptables_installed': check_iptables_installed()
    }
    
    return results

if __name__ == '__main__':
    # Configure basic logging
    logging.basicConfig(level=logging.INFO)
    
    # Direct execution for testing
    print(run())