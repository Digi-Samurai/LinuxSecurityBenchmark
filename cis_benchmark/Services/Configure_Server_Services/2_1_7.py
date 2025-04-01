import subprocess
import logging

logger = logging.getLogger(__name__)

def check_ldap_service() -> dict:
    """
    Check if LDAP server services are not in use
    CIS Benchmark 2.1.7 - Ensure ldap server services are not in use
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.1.7',
        'name': 'Ensure ldap server services are not in use',
        'status': True,  # Assume not running until proven otherwise
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check for OpenLDAP (slapd)
        slapd_installed = subprocess.run(
            "which slapd", 
            shell=True, 
            capture_output=True, 
            text=True
        )
        slapd_active = subprocess.run(
            "systemctl is-active slapd", 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # If LDAP server is found or active, it's not compliant
        if (slapd_installed.returncode == 0 or slapd_active.stdout.strip() == 'active'):
            result['status'] = False
            result['details'] = 'LDAP server (slapd) is installed or running'
            logger.warning('LDAP server service is in use')
        else:
            result['details'] = 'LDAP server services are not in use'
            logger.info('LDAP server services are not in use')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking LDAP services: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'ldap_service': check_ldap_service()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())