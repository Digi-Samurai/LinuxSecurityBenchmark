import subprocess
import logging
import os

logger = logging.getLogger(__name__)

def check_xinetd_services() -> dict:
    """
    Check if xinetd services are not in use
    CIS Benchmark 2.1.19 - Ensure xinetd services are not in use
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.1.19',
        'name': 'Ensure xinetd services are not in use',
        'status': True,  # Assume compliant until proven otherwise
        'severity': 'medium',
        'details': '',
        'services_found': []
    }
    
    try:
        # Check if xinetd is installed
        xinetd_installed_cmd = "which xinetd"
        xinetd_installed = subprocess.run(
            xinetd_installed_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if xinetd is running
        xinetd_running_cmd = "systemctl is-active xinetd"
        xinetd_running = subprocess.run(
            xinetd_running_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check xinetd configuration directory for services
        xinetd_services = []
        xinetd_config_dir = "/etc/xinetd.d"
        
        if os.path.exists(xinetd_config_dir):
            xinetd_services = [
                f for f in os.listdir(xinetd_config_dir) 
                if os.path.isfile(os.path.join(xinetd_config_dir, f))
            ]
        
        # Determine compliance
        if (xinetd_installed.returncode == 0 or 
            xinetd_running.stdout.strip() == "active" or 
            xinetd_services):
            result['status'] = False
            result['services_found'] = xinetd_services
            
            details = []
            if xinetd_installed.returncode == 0:
                details.append("Xinetd is installed")
            if xinetd_running.stdout.strip() == "active":
                details.append("Xinetd is running")
            if xinetd_services:
                details.append(f"Xinetd services found: {', '.join(xinetd_services)}")
            
            result['details'] = '; '.join(details)
            logger.warning(result['details'])
        else:
            result['details'] = 'No xinetd services detected'
            logger.info('No xinetd services detected')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking xinetd services: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'xinetd_services': check_xinetd_services()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())