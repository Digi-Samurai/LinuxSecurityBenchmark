import subprocess
import logging

logger = logging.getLogger(__name__)

def check_x_window_services() -> dict:
    """
    Check if X Window server services are in use
    CIS Benchmark 2.1.20 - Ensure X Window server services are not in use
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.1.20',
        'name': 'Ensure X Window server services are not in use',
        'status': True,  # Assumes not in use until proven otherwise
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check for X11 related services
        x_services_check_cmd = "systemctl list-unit-files | grep -E 'display-manager|gdm|lightdm|sddm|xdm'"
        x_services_result = subprocess.run(
            x_services_check_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if any X-related packages are installed
        x_packages_check_cmd = "dpkg -l | grep -E 'xserver|x11|gnome|kde|gdm|lightdm'"
        x_packages_result = subprocess.run(
            x_packages_check_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # If either command returns output, X services might be in use
        if x_services_result.stdout.strip() or x_packages_result.stdout.strip():
            result['status'] = False
            result['details'] = 'X Window server services are installed or enabled'
            logger.warning('X Window server services detected')
        else:
            result['details'] = 'No X Window server services found'
            logger.info('No X Window server services detected')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking X Window services: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'x_window_services': check_x_window_services()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())