import os
import pwd
import logging

logger = logging.getLogger(__name__)

def check_crontab_restrictions() -> dict:
    """
    Ensure crontab is restricted to authorized users
    CIS Benchmark 2.4.1.8
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.4.1.8',
        'name': 'Ensure crontab is restricted to authorized users',
        'status': True,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Paths to check for crontab restrictions
        cron_deny_path = '/etc/cron.deny'
        cron_allow_path = '/etc/cron.allow'
        
        # Check cron.deny file
        if os.path.exists(cron_deny_path):
            result['status'] = False
            result['details'] = 'cron.deny file exists, which is not recommended'
            logger.warning(result['details'])
            return result
        
        # If cron.allow doesn't exist, this might be a finding
        if not os.path.exists(cron_allow_path):
            result['status'] = False
            result['details'] = 'cron.allow file does not exist'
            logger.warning(result['details'])
            return result
        
        # Check permissions of cron.allow
        cron_allow_stat = os.stat(cron_allow_path)
        
        # Ensure cron.allow is owned by root
        if cron_allow_stat.st_uid != 0:
            result['status'] = False
            result['details'] = 'cron.allow not owned by root'
            logger.warning(result['details'])
            return result
        
        # Read allowed users
        with open(cron_allow_path, 'r') as f:
            allowed_users = f.read().splitlines()
        
        # Validate allowed users exist on the system
        for user in allowed_users:
            try:
                pwd.getpwnam(user)
            except KeyError:
                result['status'] = False
                result['details'] = f'User {user} in cron.allow does not exist'
                logger.warning(result['details'])
                return result
        
        # If all checks pass
        result['details'] = 'Crontab is properly restricted to authorized users'
        logger.info(result['details'])
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking crontab restrictions: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'crontab_restrictions': check_crontab_restrictions()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())