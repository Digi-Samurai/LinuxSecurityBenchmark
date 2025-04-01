import subprocess
import logging

logger = logging.getLogger(__name__)

def check_rsh_client() -> dict:
    """
    Check if rsh client is installed
    CIS Benchmark 2.2.2 - Ensure rsh client is not installed
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.2.2',
        'name': 'Ensure rsh Client is not installed',
        'status': False,  # False means client is installed (not compliant)
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check for rsh client packages
        package_check_commands = [
            "rpm -q rsh",    # For Red Hat/CentOS
            "dpkg -s rsh-client",   # For Debian/Ubuntu
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
                result['details'] = f'rsh client is installed. Detected by: {cmd}'
                logger.warning('rsh client is installed')
                return result
        
        # If no packages found
        result['status'] = True
        result['details'] = 'rsh client is not installed'
        logger.info('rsh client is not installed')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking rsh client: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'rsh_client': check_rsh_client()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())