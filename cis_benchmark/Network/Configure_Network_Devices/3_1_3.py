import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_bluetooth_services() -> Dict[str, Any]:
    """
    Check if Bluetooth services are not in use
    CIS Benchmark 3.1.3 - Ensure bluetooth services are not in use
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '3.1.3',
        'name': 'Ensure bluetooth services are not in use',
        'status': False,
        'severity': 'medium',
        'details': '',
        'bluetooth_services': []
    }
    
    try:
        # Check systemd bluetooth service status
        systemd_bluetooth_cmd = "systemctl is-enabled bluetooth 2>/dev/null"
        systemd_result = subprocess.run(
            systemd_bluetooth_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check loaded kernel modules
        kernel_modules_cmd = "lsmod | grep -i bluetooth"
        kernel_modules_result = subprocess.run(
            kernel_modules_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check for running Bluetooth processes
        bluetooth_processes_cmd = "ps aux | grep -i '[b]luetooth'"
        processes_result = subprocess.run(
            bluetooth_processes_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Collect Bluetooth-related information
        bluetooth_services = []
        
        # Check systemd service
        if 'enabled' in systemd_result.stdout.lower():
            bluetooth_services.append('Systemd Bluetooth Service')
        
        # Check kernel modules
        if kernel_modules_result.stdout.strip():
            bluetooth_services.extend(
                module.split()[0] for module in kernel_modules_result.stdout.split('\n') 
                if module.strip()
            )
        
        # Check running processes
        if processes_result.stdout.strip():
            bluetooth_services.append('Bluetooth Processes Running')
        
        # Store found services
        result['bluetooth_services'] = bluetooth_services
        
        # Determine compliance
        if not bluetooth_services:
            result['status'] = True
            result['details'] = 'No Bluetooth services or modules found'
        else:
            result['details'] = f'Bluetooth services found: {", ".join(bluetooth_services)}'
        
        logger.info(result['details'])
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking Bluetooth services: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'bluetooth_services': check_bluetooth_services()
    }
    
    return results

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Direct execution for testing
    results = run()
    print(results['bluetooth_services'])