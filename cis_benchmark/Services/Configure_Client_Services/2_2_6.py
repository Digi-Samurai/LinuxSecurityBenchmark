import subprocess
import logging

logger = logging.getLogger(__name__)

def check_ftp_client() -> dict:
    """
    Check if ftp client is installed
    CIS Benchmark 2.2.6 - Ensure ftp client is not installed
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.2.6',
        'name': 'Ensure ftp Client is not installed',
        'status': False,  # False means client is installed (not compliant)
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check for ftp client packages
        package_check_commands = [
            "rpm -q ftp",    # For Red Hat/CentOS
            "dpkg -s ftp",   # For Debian/Ubuntu
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
                result['details'] = f'ftp client is installed. Detected by: {cmd}'
                logger.warning('ftp client is installed')
                return result
        
        # If no packages found
        result['status'] = True
        result['details'] = 'ftp client is not installed'
        logger.info('ftp client is not installed')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking ftp client: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'ftp_client': check_ftp_client()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())