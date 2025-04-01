import os
import stat
import logging

logger = logging.getLogger(__name__)

def check_cron_monthly_permissions() -> dict:
    """
    Ensure permissions on /etc/cron.monthly are configured
    CIS Benchmark 2.4.1.6
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.4.1.6',
        'name': 'Ensure permissions on /etc/cron.monthly are configured',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Path to check
        cron_monthly_path = '/etc/cron.monthly'
        
        # Check if directory exists
        if not os.path.exists(cron_monthly_path):
            result['details'] = '/etc/cron.monthly directory does not exist'
            logger.warning(result['details'])
            return result
        
        # Get directory stats
        dir_stat = os.stat(cron_monthly_path)
        
        # Check owner (should be root)
        if dir_stat.st_uid != 0:
            result['details'] = 'Directory not owned by root'
            logger.warning(result['details'])
            return result
        
        # Check group (should be root)
        if dir_stat.st_gid != 0:
            result['details'] = 'Directory group not set to root'
            logger.warning(result['details'])
            return result
        
        # Check permissions (should be 700)
        dir_mode = stat.S_IMODE(dir_stat.st_mode)
        if dir_mode != 0o700:
            result['details'] = f'Incorrect permissions. Current: {oct(dir_mode)}, Expected: 0o700'
            logger.warning(result['details'])
            return result
        
        # If all checks pass
        result['status'] = True
        result['details'] = 'Cron monthly directory permissions are correctly configured'
        logger.info(result['details'])
    
    except Exception as e:
        result['details'] = f'Error checking cron monthly permissions: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'cron_monthly_permissions': check_cron_monthly_permissions()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())