import subprocess
import logging

logger = logging.getLogger(__name__)

def check_devshm_nodev() -> dict:
    """
    Check if nodev option is set on /dev/shm partition
    CIS Benchmark 1.1.2.2.2 - Ensure nodev option set on /dev/shm partition
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.1.2.2.2',
        'name': 'Ensure nodev option set on /dev/shm partition',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Use mount command to check mount options
        mount_cmd = "mount | grep /dev/shm"
        mount_result = subprocess.run(
            mount_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if nodev option is present
        if mount_result.returncode == 0:
            mount_output = mount_result.stdout.strip()
            if 'nodev' in mount_output:
                result['status'] = True
                result['details'] = '/dev/shm is mounted with nodev option'
                logger.info('/dev/shm is mounted with nodev option')
            else:
                result['status'] = False
                result['details'] = '/dev/shm is not mounted with nodev option'
                logger.warning('/dev/shm is not mounted with nodev option')
        else:
            result['status'] = False
            result['details'] = 'Could not retrieve /dev/shm mount information'
            logger.error('Could not retrieve /dev/shm mount information')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking /dev/shm nodev option: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'devshm_nodev': check_devshm_nodev()
    }
    
    return results

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Direct execution for testing
    print(run())