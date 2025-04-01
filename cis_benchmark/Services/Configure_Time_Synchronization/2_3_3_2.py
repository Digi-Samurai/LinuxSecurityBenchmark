import subprocess
import logging
import pwd

logger = logging.getLogger(__name__)

def check_chrony_user() -> dict:
    """
    Ensure chrony is running as user _chrony
    CIS Benchmark 2.3.3.2
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.3.3.2',
        'name': 'Ensure chrony is running as user _chrony',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check if _chrony user exists
        try:
            pwd.getpwnam('_chrony')
            chrony_user_exists = True
        except KeyError:
            chrony_user_exists = False
        
        # Get chrony process details
        ps_cmd = "ps -C chronyd -o user="
        ps_result = subprocess.run(
            ps_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Process the result
        if ps_result.returncode == 0:
            running_user = ps_result.stdout.strip()
            
            # Check if running as _chrony
            if running_user == '_chrony':
                result['status'] = True
                result['details'] = 'Chrony is running as _chrony user'
                logger.info('Chrony is running as _chrony user')
            else:
                result['details'] = f'Chrony is running as {running_user}, not _chrony'
                logger.warning(f'Chrony is running as {running_user}')
        else:
            result['details'] = 'Chrony process not found'
            logger.warning('Chrony process not running')
        
        # Additional check for _chrony user existence
        if not chrony_user_exists:
            result['details'] += '. _chrony user does not exist'
            logger.warning('_chrony user does not exist')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking chrony user: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'chrony_user': check_chrony_user()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())