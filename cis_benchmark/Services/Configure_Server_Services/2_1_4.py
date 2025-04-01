import subprocess
import logging

logger = logging.getLogger(__name__)

def check_dns_service() -> dict:
    """
    Check if DNS server services are not in use
    CIS Benchmark 2.1.4 - Ensure dns server services are not in use
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.1.4',
        'name': 'Ensure dns server services are not in use',
        'status': True,  # Assume compliant until proven otherwise
        'severity': 'medium',
        'details': ''
    }
    
    # List of potential DNS server packages and services
    dns_services = [
        'bind9',        # Ubuntu/Debian
        'named',        # Red Hat/CentOS
        'bind',         # Some distributions
    ]
    
    try:
        # Check for installed packages
        for service in dns_services:
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
        
        # If no details were added, it means no DNS services were found
        if not result['details']:
            result['details'] = 'No DNS server services found'
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking DNS services: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'dns_service': check_dns_service()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())