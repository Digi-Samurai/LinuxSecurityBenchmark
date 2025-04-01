import subprocess
import logging

logger = logging.getLogger(__name__)

def check_talk_client() -> dict:
    """
    Check if talk client is installed
    CIS Benchmark 2.2.3 - Ensure talk client is not installed
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.2.3',
        'name': 'Ensure talk Client is not installed',
        'status': False,  # False means client is installed (not compliant)
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check for talk client packages
        package_check_commands = [
            "rpm -q talk",    # For Red Hat/CentOS
            "dpkg -s talk",   # For Debian/Ubuntu
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
                result['details'] = f'talk client is installed. Detected by: {cmd}'
                logger.warning('talk client is installed')
                return result
        
        # If no packages found
        result['status'] = True
        result['details'] = 'talk client is not installed'
        logger.info('talk client is not installed')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking talk client: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'talk_client': check_talk_client()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())