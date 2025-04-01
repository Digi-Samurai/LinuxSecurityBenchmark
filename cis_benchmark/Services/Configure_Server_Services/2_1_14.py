import subprocess
import logging

logger = logging.getLogger(__name__)

def check_samba_services() -> dict:
    """
    Check if Samba file server services are in use
    CIS Benchmark 2.1.14 - Ensure samba file server services are not in use
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.1.14',
        'name': 'Ensure samba file server services are not in use',
        'status': True,  # True means services are NOT in use
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check if Samba-related services are installed or running
        samba_services = [
            'smbd',  # Samba daemon
            'nmbd',  # Netbios name service
            'samba'  # General Samba service
        ]
        
        service_check_commands = [
            "systemctl is-active {}",
            "systemctl is-enabled {}",
            "dpkg -s samba || rpm -q samba"
        ]
        
        for service in samba_services:
            for cmd_template in service_check_commands:
                cmd = cmd_template.format(service)
                try:
                    result_output = subprocess.run(
                        cmd, 
                        shell=True, 
                        capture_output=True, 
                        text=True
                    )
                    
                    # If any command returns a success status, service is in use
                    if result_output.returncode == 0:
                        result['status'] = False
                        result['details'] += f"Samba service {service} is active or installed. "
                        logger.warning(f"Samba service {service} is active or installed")
                except Exception as e:
                    logger.error(f"Error checking Samba service {service}: {e}")
        
        # If no services found, set details accordingly
        if result['status']:
            result['details'] = 'No Samba services found'
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking Samba services: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'samba_services': check_samba_services()
    }
    
    return results

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Direct execution for testing
    print(run())