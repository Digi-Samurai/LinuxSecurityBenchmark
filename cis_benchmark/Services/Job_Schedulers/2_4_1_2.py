import os
import stat
import logging

logger = logging.getLogger(__name__)

def check_crontab_permissions() -> dict:
    """
    Check permissions on /etc/crontab
    CIS Benchmark 2.4.1.2 - Ensure permissions on /etc/crontab are configured
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.4.1.2',
        'name': 'Ensure permissions on /etc/crontab are configured',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    crontab_path = '/etc/crontab'
    
    try:
        # Check if file exists
        if not os.path.exists(crontab_path):
            result['details'] = '/etc/crontab does not exist'
            return result
        
        # Get file stats
        file_stat = os.stat(crontab_path)
        
        # Check ownership (should be root:root)
        uid = file_stat.st_uid
        gid = file_stat.st_gid
        
        # Check permissions (should be 0600 or 0644)
        file_mode = stat.S_IMODE(file_stat.st_mode)
        
        # Check for root ownership and correct permissions
        owner = os.stat(crontab_path).st_uid == 0
        group = os.stat(crontab_path).st_gid == 0
        permissions = file_mode in [0o600, 0o644]
        
        if owner and group and permissions:
            result['status'] = True
            result['details'] = f'Correct permissions: {oct(file_mode)}'
            logger.info('Crontab permissions are correctly configured')
        else:
            result['details'] = (
                f'Incorrect configuration: '
                f'Owner: {uid}, Group: {gid}, Permissions: {oct(file_mode)}'
            )
            logger.warning('Crontab permissions are not correctly configured')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking crontab permissions: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'crontab_permissions': check_crontab_permissions()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())