import subprocess
import logging
import re

logger = logging.getLogger(__name__)

def check_mta_local_only() -> dict:
    """
    Check if Mail Transfer Agent is configured for local-only mode
    CIS Benchmark 2.1.21 - Ensure mail transfer agent is configured for local-only mode
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.1.21',
        'name': 'Ensure mail transfer agent is configured for local-only mode',
        'status': False,  # Assumes not compliant until proven
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check for MTA services
        mta_services = ['postfix', 'sendmail', 'exim4']
        
        for mta in mta_services:
            # Check if MTA is installed
            installed_check_cmd = f"dpkg -l | grep {mta}"
            installed_result = subprocess.run(
                installed_check_cmd, 
                shell=True, 
                capture_output=True, 
                text=True
            )
            
            if installed_result.stdout.strip():
                # If Postfix, check its configuration
                if mta == 'postfix':
                    inet_interfaces_cmd = "postconf -n inet_interfaces"
                    inet_interfaces_result = subprocess.run(
                        inet_interfaces_cmd, 
                        shell=True, 
                        capture_output=True, 
                        text=True
                    )
                    
                    # Check if inet_interfaces is set to localhost
                    if re.search(r'inet_interfaces\s*=\s*localhost', inet_interfaces_result.stdout):
                        result['status'] = True
                        result['details'] = 'Postfix is configured for local-only mode'
                        logger.info('Postfix is configured for local-only mode')
                        break
                    else:
                        result['details'] = f'{mta.capitalize()} is not configured for local-only mode'
                        logger.warning(f'{mta.capitalize()} is not configured for local-only mode')
                
                # For other MTAs, we might need more specific checks
                else:
                    result['details'] = f'Additional configuration check needed for {mta}'
                    logger.warning(f'Additional configuration check needed for {mta}')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking Mail Transfer Agent: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'mta_local_only': check_mta_local_only()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())