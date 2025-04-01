import subprocess
import logging

logger = logging.getLogger(__name__)

def check_rsync_services() -> dict:
    """
    Check if rsync services are not in use
    CIS Benchmark 2.1.13 - Ensure rsync services are not in use
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.1.13',
        'name': 'Ensure rsync services are not in use',
        'status': False,  # False means services are available (not compliant)
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check if rsync services are installed or running
        rsync_services = [
            'rsync',
            'rsyncd'
        ]
        
        # Check service status using systemctl
        systemctl_cmd = f"systemctl is-active {' '.join(rsync_services)}"
        systemctl_result = subprocess.run(
            systemctl_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check package installation
        package_check_cmd = f"dpkg -l {' '.join(rsync_services)} || rpm -q {' '.join(rsync_services)}"
        package_result = subprocess.run(
            package_check_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Determine if rsync services are in use
        if systemctl_result.returncode == 0 or package_result.returncode == 0:
            result['status'] = False
            result['details'] = 'RSync services are installed or running'
            logger.warning('RSync services are installed or running')
        else:
            result['status'] = True
            result['details'] = 'RSync services are not in use'
            logger.info('RSync services are not in use')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking RSync services: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'rsync_services': check_rsync_services()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())