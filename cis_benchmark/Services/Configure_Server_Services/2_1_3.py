import subprocess
import logging

logger = logging.getLogger(__name__)

def check_dhcp_service() -> dict:
    """
    Check if DHCP server services are not in use
    CIS Benchmark 2.1.3 - Ensure dhcp server services are not in use
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.1.3',
        'name': 'Ensure dhcp server services are not in use',
        'status': True,  # Assume compliant until proven otherwise
        'severity': 'medium',
        'details': ''
    }
    
    # List of potential DHCP server packages and services
    dhcp_services = [
        'isc-dhcp-server',  # Ubuntu/Debian
        'dhcpd',            # Red Hat/CentOS
        'dhcp',             # Some distributions
    ]
    
    try:
        # Check for installed packages
        for service in dhcp_services:
            # Check if package is installed
            pkg_check_cmd = f"dpkg -s {service} 2>/dev/null || rpm -q {service} 2>/dev/null"
            pkg_result = subprocess.run(
                pkg_check_cmd, 
                shell=True, 
                capture_output=True, 
                text=True
            )
            
            # Check if service is running
            service_check_cmd = f"systemctl is-active {service} 2>/dev/null"
            service_result = subprocess.run(
                service_check_cmd, 
                shell=True, 
                capture_output=True, 
                text=True
            )
            
            # If package is installed or service is active, it's not compliant
            if pkg_result.returncode == 0 or 'active' in service_result.stdout:
                result['status'] = False
                result['details'] += f"{service} service is installed or running. "
                logger.warning(f"{service} service is installed or running")
        
        # If no details were added, it means no DHCP services were found
        if not result['details']:
            result['details'] = 'No DHCP server services found'
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking DHCP services: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'dhcp_service': check_dhcp_service()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())