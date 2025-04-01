import subprocess
import logging

logger = logging.getLogger(__name__)

def check_print_server_services() -> dict:
    """
    Check if print server services are not in use
    CIS Benchmark 2.1.11 - Ensure print server services are not in use
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.1.11',
        'name': 'Ensure print server services are not in use',
        'status': False,  # False means services are available (not compliant)
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check if print server services are installed or running
        print_services = [
            'cups',           # Common Unix Printing System
            'cups-browsed',   # Additional CUPS service
            'lpd',            # Line Printer Daemon
            'printer'         # Generic printer service
        ]
        
        # Check service status using systemctl
        systemctl_cmd = f"systemctl is-active {' '.join(print_services)}"
        systemctl_result = subprocess.run(
            systemctl_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check package installation
        package_check_cmd = f"dpkg -l {' '.join(print_services)} || rpm -q {' '.join(print_services)}"
        package_result = subprocess.run(
            package_check_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Determine if print server services are in use
        if systemctl_result.returncode == 0 or package_result.returncode == 0:
            result['status'] = False
            result['details'] = 'Print server services are installed or running'
            logger.warning('Print server services are installed or running')
        else:
            result['status'] = True
            result['details'] = 'Print server services are not in use'
            logger.info('Print server services are not in use')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking print server services: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'print_server_services': check_print_server_services()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())