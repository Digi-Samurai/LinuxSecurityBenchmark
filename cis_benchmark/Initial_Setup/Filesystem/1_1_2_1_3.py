import subprocess
import logging

logger = logging.getLogger(__name__)

def check_tmp_nosuid_option() -> dict:
    """
    Check if nosuid option is set on /tmp partition
    CIS Benchmark 1.1.2.1.3 - Ensure nosuid option set on /tmp partition
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.1.2.1.3',
        'name': 'Ensure nosuid option set on /tmp partition',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Use mount command to check /tmp mount options
        mount_cmd = "mount | grep ' /tmp '"
        mount_result = subprocess.run(
            mount_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if nosuid option is present
        if mount_result.stdout and 'nosuid' in mount_result.stdout:
            result['status'] = True
            result['details'] = 'nosuid option is set on /tmp partition'
            logger.info('nosuid option is set on /tmp partition')
        else:
            result['status'] = False
            result['details'] = 'nosuid option is not set on /tmp partition'
            logger.warning('nosuid option is not set on /tmp partition')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking /tmp nosuid option: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'tmp_nosuid_option': check_tmp_nosuid_option()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())