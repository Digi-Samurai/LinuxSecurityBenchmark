import subprocess
import logging

logger = logging.getLogger(__name__)

def check_nis_client() -> dict:
    """
    Check if NIS (Network Information Service) client is installed
    CIS Benchmark 2.2.1 - Ensure NIS Client is not installed
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.2.1',
        'name': 'Ensure NIS Client is not installed',
        'status': False,  # False means client is installed (not compliant)
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check for NIS client packages
        package_check_commands = [
            "rpm -q ypbind",  # For Red Hat/CentOS
            "dpkg -s nis",   # For Debian/Ubuntu
        ]
        
        for cmd in package_check_commands:
            package_result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True
            )
            
            # If any command returns a non-empty output, the package is installed
            if package_result.stdout.strip() or package_result.returncode == 0:
                result['status'] = False
                result['details'] = f'NIS client is installed. Detected by: {cmd}'
                logger.warning('NIS client is installed')
                return result
        
        # If no packages found
        result['status'] = True
        result['details'] = 'NIS client is not installed'
        logger.info('NIS client is not installed')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking NIS client: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'nis_client': check_nis_client()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())