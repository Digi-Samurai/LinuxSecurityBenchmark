import subprocess
import logging

logger = logging.getLogger(__name__)

def check_ldap_client() -> dict:
    """
    Check if ldap client is installed
    CIS Benchmark 2.2.5 - Ensure ldap client is not installed
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.2.5',
        'name': 'Ensure ldap Client is not installed',
        'status': False,  # False means client is installed (not compliant)
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check for ldap client packages
        package_check_commands = [
            "rpm -q openldap-clients",    # For Red Hat/CentOS
            "dpkg -s ldap-utils",   # For Debian/Ubuntu
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
                result['details'] = f'ldap client is installed. Detected by: {cmd}'
                logger.warning('ldap client is installed')
                return result
        
        # If no packages found
        result['status'] = True
        result['details'] = 'ldap client is not installed'
        logger.info('ldap client is not installed')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking ldap client: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'ldap_client': check_ldap_client()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())