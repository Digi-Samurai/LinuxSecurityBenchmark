import subprocess
import logging

logger = logging.getLogger(__name__)

def check_rpcbind_services() -> dict:
    """
    Check if rpcbind services are not in use
    CIS Benchmark 2.1.12 - Ensure rpcbind services are not in use
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.1.12',
        'name': 'Ensure rpcbind services are not in use',
        'status': False,  # False means services are available (not compliant)
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check if rpcbind services are installed or running
        rpcbind_services = [
            'rpcbind',
            'portmap'
        ]
        
        # Check service status using systemctl
        systemctl_cmd = f"systemctl is-active {' '.join(rpcbind_services)}"
        systemctl_result = subprocess.run(
            systemctl_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check package installation
        package_check_cmd = f"dpkg -l {' '.join(rpcbind_services)} || rpm -q {' '.join(rpcbind_services)}"
        package_result = subprocess.run(
            package_check_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Determine if rpcbind services are in use
        if systemctl_result.returncode == 0 or package_result.returncode == 0:
            result['status'] = False
            result['details'] = 'RPC Bind services are installed or running'
            logger.warning('RPC Bind services are installed or running')
        else:
            result['status'] = True
            result['details'] = 'RPC Bind services are not in use'
            logger.info('RPC Bind services are not in use')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking RPC Bind services: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'rpcbind_services': check_rpcbind_services()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())