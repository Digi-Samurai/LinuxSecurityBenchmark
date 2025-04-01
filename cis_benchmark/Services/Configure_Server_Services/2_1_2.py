import subprocess
import logging

logger = logging.getLogger(__name__)

def check_avahi_service() -> dict:
    """
    Check if avahi-daemon service is installed and running
    CIS Benchmark 2.1.2
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.1.2',
        'name': 'Ensure avahi daemon services are not in use',
        'status': True,  # True means service is NOT in use (compliant)
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check if avahi-daemon is installed
        rpm_check_cmd = "rpm -q avahi"
        rpm_result = subprocess.run(
            rpm_check_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if avahi-daemon service is active
        systemctl_check_cmd = "systemctl is-active avahi-daemon"
        systemctl_result = subprocess.run(
            systemctl_check_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Determine if service is in use
        is_service_in_use = (
            rpm_result.returncode == 0 or  # Package is installed
            'active' in systemctl_result.stdout.lower()
        )
        
        if is_service_in_use:
            result['status'] = False
            result['details'] = 'Avahi daemon service is installed or running'
            logger.warning('Avahi daemon service is in use')
        else:
            result['status'] = True
            result['details'] = 'Avahi daemon service is not in use'
            logger.info('Avahi daemon service is not in use')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking avahi daemon service: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run avahi daemon service check
    
    :return: Dictionary of check results
    """
    results = {
        'avahi_service': check_avahi_service()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())