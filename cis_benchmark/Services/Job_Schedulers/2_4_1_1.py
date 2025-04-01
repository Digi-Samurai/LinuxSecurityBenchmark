import subprocess
import logging

logger = logging.getLogger(__name__)

def check_cron_daemon_status() -> dict:
    """
    Check if cron daemon is enabled and active
    CIS Benchmark 2.4.1.1 - Ensure cron daemon is enabled and active
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.4.1.1',
        'name': 'Ensure cron daemon is enabled and active',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check if crond service is active and enabled
        active_cmd = "systemctl is-active cron || systemctl is-active crond"
        enabled_cmd = "systemctl is-enabled cron || systemctl is-enabled crond"
        
        active_result = subprocess.run(
            active_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        enabled_result = subprocess.run(
            enabled_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if service is both active and enabled
        if (active_result.stdout.strip() == 'active' and 
            enabled_result.stdout.strip() == 'enabled'):
            result['status'] = True
            result['details'] = 'Cron daemon is enabled and active'
            logger.info('Cron daemon is enabled and active')
        else:
            result['status'] = False
            result['details'] = (
                f'Cron daemon active status: {active_result.stdout.strip()}, '
                f'enabled status: {enabled_result.stdout.strip()}'
            )
            logger.warning('Cron daemon is not fully enabled and active')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking cron daemon: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'cron_daemon_status': check_cron_daemon_status()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())