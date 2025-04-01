import subprocess
import logging

logger = logging.getLogger(__name__)

def check_message_access_service() -> dict:
    """
    Check if message access server services are not in use
    CIS Benchmark 2.1.8 - Ensure message access server services are not in use
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.1.8',
        'name': 'Ensure message access server services are not in use',
        'status': True,  # Assume not running until proven otherwise
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check for common message access servers
        servers_to_check = [
            'dovecot',    # IMAP/POP3 server
            'cyrus-imapd' # Another IMAP server
        ]
        
        for server in servers_to_check:
            # Check if server is installed
            installed_check = subprocess.run(
                f"which {server}", 
                shell=True, 
                capture_output=True, 
                text=True
            )
            
            # Check if server service is active
            service_check = subprocess.run(
                f"systemctl is-active {server}", 
                shell=True, 
                capture_output=True, 
                text=True
            )
            
            # If server is found or service is active, it's not compliant
            if installed_check.returncode == 0 or service_check.stdout.strip() == 'active':
                result['status'] = False
                result['details'] = f'Message access server ({server}) is installed or running'
                logger.warning(f'{server} service is in use')
                break
        
        if result['status']:
            result['details'] = 'Message access server services are not in use'
            logger.info('Message access server services are not in use')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking message access services: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'message_access_service': check_message_access_service()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())