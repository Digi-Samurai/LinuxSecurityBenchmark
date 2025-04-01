import subprocess
import logging

logger = logging.getLogger(__name__)

def check_web_proxy_services() -> dict:
    """
    Check if Web Proxy services are in use
    CIS Benchmark 2.1.17 - Ensure web proxy server services are not in use
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.1.17',
        'name': 'Ensure web proxy server services are not in use',
        'status': True,  # True means services are NOT in use
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check if Web Proxy-related services are installed or running
        web_proxy_services = [
            'squid',  # Squid proxy server
            'tinyproxy',  # Tiny proxy server
            'privoxy'  # Privacy enhancing proxy
        ]
        
        service_check_commands = [
            "systemctl is-active {}",
            "systemctl is-enabled {}",
            "dpkg -s {} || rpm -q {}"
        ]
        
        for service in web_proxy_services:
            for cmd_template in service_check_commands:
                # Try both service name and package name
                cmd = cmd_template.format(service, service)
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
                        result['details'] += f"Web Proxy service {service} is active or installed. "
                        logger.warning(f"Web Proxy service {service} is active or installed")
                except Exception as e:
                    logger.error(f"Error checking Web Proxy service {service}: {e}")
        
        # If no services found, set details accordingly
        if result['status']:
            result['details'] = 'No Web Proxy services found'
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking Web Proxy services: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'web_proxy_services': check_web_proxy_services()
    }
    
    return results

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Direct execution for testing
    print(run())