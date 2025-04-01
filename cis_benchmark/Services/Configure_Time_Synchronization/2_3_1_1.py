import subprocess
import logging

logger = logging.getLogger(__name__)

def check_single_time_sync_daemon() -> dict:
    """
    Ensure a single time synchronization daemon is in use
    CIS Benchmark 2.3.1.1
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.3.1.1',
        'name': 'Ensure a single time synchronization daemon is in use',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # List of common time sync daemons
        time_sync_daemons = [
            'chronyd',
            'ntpd',
            'systemd-timesyncd'
        ]
        
        # Check which time sync daemons are active
        active_daemons = []
        
        for daemon in time_sync_daemons:
            # Check if daemon is installed and active
            status_cmd = f"systemctl is-active {daemon}"
            status_result = subprocess.run(
                status_cmd, 
                shell=True, 
                capture_output=True, 
                text=True
            )
            
            if status_result.returncode == 0:
                active_daemons.append(daemon)
        
        # Check if only one daemon is active
        if len(active_daemons) == 1:
            result['status'] = True
            result['details'] = f'Single time sync daemon in use: {active_daemons[0]}'
            logger.info(f'Single time sync daemon found: {active_daemons[0]}')
        elif len(active_daemons) > 1:
            result['status'] = False
            result['details'] = f'Multiple time sync daemons active: {", ".join(active_daemons)}'
            logger.warning(f'Multiple time sync daemons found: {active_daemons}')
        else:
            result['status'] = False
            result['details'] = 'No time sync daemon found'
            logger.warning('No time sync daemon is active')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking time sync daemon: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'single_time_sync_daemon': check_single_time_sync_daemon()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())