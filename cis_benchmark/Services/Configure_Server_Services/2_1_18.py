import subprocess
import logging

logger = logging.getLogger(__name__)

def check_web_server_services() -> dict:
    """
    Check if web server services are not in use
    CIS Benchmark 2.1.18 - Ensure web server services are not in use
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.1.18',
        'name': 'Ensure web server services are not in use',
        'status': True,  # Assume compliant until proven otherwise
        'severity': 'medium',
        'details': '',
        'services_found': []
    }
    
    # List of common web server services to check
    web_server_services = [
        'apache2',
        'httpd',
        'nginx',
        'lighttpd',
        'tomcat',
        'jetty'
    ]
    
    try:
        # Check systemd services
        systemd_cmd = "systemctl list-unit-files --type=service | grep -E '(httpd|apache2|nginx|lighttpd|tomcat|jetty)'"
        systemd_result = subprocess.run(
            systemd_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check running services
        running_cmd = "systemctl list-units --type=service --state=running | grep -E '(httpd|apache2|nginx|lighttpd|tomcat|jetty)'"
        running_result = subprocess.run(
            running_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Compile list of found services
        found_services = []
        
        # Check systemd unit files
        if systemd_result.stdout.strip():
            for line in systemd_result.stdout.split('\n'):
                for service in web_server_services:
                    if service in line.lower():
                        found_services.append(line.split()[0])
        
        # Check running services
        if running_result.stdout.strip():
            for line in running_result.stdout.split('\n'):
                for service in web_server_services:
                    if service in line.lower():
                        found_services.append(line.split()[0])
        
        # Remove duplicates
        found_services = list(set(found_services))
        
        # Update result
        if found_services:
            result['status'] = False
            result['services_found'] = found_services
            result['details'] = f"Web server services found: {', '.join(found_services)}"
            logger.warning(f"Web server services detected: {found_services}")
        else:
            result['details'] = 'No web server services found'
            logger.info('No web server services detected')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking web server services: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'web_server_services': check_web_server_services()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())