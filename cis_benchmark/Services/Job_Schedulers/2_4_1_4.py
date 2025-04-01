import os
import stat
import logging

logger = logging.getLogger(__name__)

def check_cron_daily_permissions() -> dict:
    """
    Check permissions on /etc/cron.daily
    CIS Benchmark 2.4.1.4 - Ensure permissions on /etc/cron.daily are configured
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.4.1.4',
        'name': 'Ensure permissions on /etc/cron.daily are configured',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    cron_daily_path = '/etc/cron.daily'
    
    try:
        # Check if directory exists
        if not os.path.exists(cron_daily_path):
            result['details'] = '/etc/cron.daily does not exist'
            return result
        
        # Get directory stats
        dir_stat = os.stat(cron_daily_path)
        
        # Check ownership (should be root:root)
        uid = dir_stat.st_uid
        gid = dir_stat.st_gid
        
        # Check directory permissions (should be 0755)
        dir_mode = stat.S_IMODE(dir_stat.st_mode)
        
        # Check for root ownership and correct permissions
        owner = uid == 0
        group = gid == 0
        permissions = dir_mode == 0o755
        
        if owner and group and permissions:
            result['status'] = True
            result['details'] = f'Correct permissions: {oct(dir_mode)}'
            logger.info('Cron daily directory permissions are correctly configured')
        else:
            result['details'] = (
                f'Incorrect configuration: '
                f'Owner: {uid}, Group: {gid}, Permissions: {oct(dir_mode)}'
            )
            logger.warning('Cron daily directory permissions are not correctly configured')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking cron daily permissions: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'cron_daily_permissions': check_cron_daily_permissions()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())