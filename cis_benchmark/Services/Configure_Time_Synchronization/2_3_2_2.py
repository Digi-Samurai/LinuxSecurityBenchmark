import subprocess
import logging

logger = logging.getLogger(__name__)

def check_timesyncd_status() -> dict:
    """
    Ensure systemd-timesyncd is enabled and running
    CIS Benchmark 2.3.2.2
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.3.2.2',
        'name': 'Ensure systemd-timesyncd is enabled and running',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check if timesyncd is enabled
        enabled_cmd = "systemctl is-enabled systemd-timesyncd"
        enabled_result = subprocess.run(
            enabled_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if timesyncd is active
        active_cmd = "systemctl is-active systemd-timesyncd"
        active_result = subprocess.run(
            active_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Evaluate results
        is_enabled = enabled_result.returncode == 0
        is_active = active_result.returncode == 0
        
        if is_enabled and is_active:
            result['status'] = True
            result['details'] = 'Systemd-timesyncd is enabled and running'
            logger.info('Systemd-timesyncd is enabled and running')
        else:
            details = []
            if not is_enabled:
                details.append('Systemd-timesyncd is not enabled')
            if not is_active:
                details.append('Systemd-timesyncd is not running')
            
            result['details'] = ', '.join(details)
            logger.warning(result['details'])
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking systemd-timesyncd status: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'timesyncd_status': check_timesyncd_status()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())