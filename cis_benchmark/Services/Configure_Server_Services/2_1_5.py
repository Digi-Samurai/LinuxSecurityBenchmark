import subprocess
import logging

logger = logging.getLogger(__name__)

def check_dnsmasq_service() -> dict:
    """
    Check if dnsmasq service is not in use
    CIS Benchmark 2.1.5 - Ensure dnsmasq services are not in use
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.1.5',
        'name': 'Ensure dnsmasq services are not in use',
        'status': True,  # Assume not running until proven otherwise
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check if dnsmasq is installed
        installed_check = subprocess.run(
            "which dnsmasq", 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if dnsmasq service is active
        service_check = subprocess.run(
            "systemctl is-active dnsmasq", 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # If dnsmasq is found or service is active, it's not compliant
        if installed_check.returncode == 0 or service_check.stdout.strip() == 'active':
            result['status'] = False
            result['details'] = 'dnsmasq is installed or running'
            logger.warning('dnsmasq service is in use')
        else:
            result['details'] = 'dnsmasq service is not in use'
            logger.info('dnsmasq service is not in use')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking dnsmasq: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'dnsmasq_service': check_dnsmasq_service()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())