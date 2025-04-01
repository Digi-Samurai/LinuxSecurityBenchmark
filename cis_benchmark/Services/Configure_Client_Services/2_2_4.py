import subprocess
import logging

logger = logging.getLogger(__name__)

def check_telnet_client() -> dict:
    """
    Check if telnet client is installed
    CIS Benchmark 2.2.4 - Ensure telnet client is not installed
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.2.4',
        'name': 'Ensure telnet Client is not installed',
        'status': False,  # False means client is installed (not compliant)
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check for telnet client packages
        package_check_commands = [
            "rpm -q telnet",    # For Red Hat/CentOS
            "dpkg -s telnet",   # For Debian/Ubuntu
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
                result['details'] = f'telnet client is installed. Detected by: {cmd}'
                logger.warning('telnet client is installed')
                return result
        
        # If no packages found
        result['status'] = True
        result['details'] = 'telnet client is not installed'
        logger.info('telnet client is not installed')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking telnet client: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'telnet_client': check_telnet_client()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())