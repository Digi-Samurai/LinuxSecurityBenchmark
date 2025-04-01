import subprocess
import logging

logger = logging.getLogger(__name__)

def check_tftp_services() -> dict:
    """
    Check if TFTP services are in use
    CIS Benchmark 2.1.16 - Ensure tftp server services are not in use
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.1.16',
        'name': 'Ensure tftp server services are not in use',
        'status': True,  # True means services are NOT in use
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check if TFTP-related services are installed or running
        tftp_services = [
            'tftpd',  # TFTP daemon
            'atftpd'  # Advanced TFTP daemon
        ]
        
        service_check_commands = [
            "systemctl is-active {}",
            "systemctl is-enabled {}",
            "dpkg -s tftpd || rpm -q tftp-server"
        ]
        
        for service in tftp_services:
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
                        result['details'] += f"TFTP service {service} is active or installed. "
                        logger.warning(f"TFTP service {service} is active or installed")
                except Exception as e:
                    logger.error(f"Error checking TFTP service {service}: {e}")
        
        # If no services found, set details accordingly
        if result['status']:
            result['details'] = 'No TFTP services found'
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking TFTP services: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'tftp_services': check_tftp_services()
    }
    
    return results

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Direct execution for testing
    print(run())