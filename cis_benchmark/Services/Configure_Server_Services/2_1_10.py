import subprocess
import logging

logger = logging.getLogger(__name__)

def check_nis_services() -> dict:
    """
    Check if NIS (Network Information Service) server services are not in use
    CIS Benchmark 2.1.10 - Ensure nis server services are not in use
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.1.10',
        'name': 'Ensure nis server services are not in use',
        'status': False,  # False means services are available (not compliant)
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check if NIS services are installed or running
        nis_services = [
            'nis',
            'yp-tools',
            'ypserv',
            'ypbind'
        ]
        
        # Check service status using systemctl
        systemctl_cmd = f"systemctl is-active {' '.join(nis_services)}"
        systemctl_result = subprocess.run(
            systemctl_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check package installation
        package_check_cmd = f"dpkg -l {' '.join(nis_services)} || rpm -q {' '.join(nis_services)}"
        package_result = subprocess.run(
            package_check_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Determine if NIS services are in use
        if systemctl_result.returncode == 0 or package_result.returncode == 0:
            result['status'] = False
            result['details'] = 'NIS services are installed or running'
            logger.warning('NIS services are installed or running')
        else:
            result['status'] = True
            result['details'] = 'NIS services are not in use'
            logger.info('NIS services are not in use')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking NIS services: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'nis_services': check_nis_services()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())