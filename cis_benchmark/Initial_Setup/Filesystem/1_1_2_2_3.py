import subprocess
import logging

logger = logging.getLogger(__name__)

def check_devshm_nosuid() -> dict:
    """
    Check if nosuid option is set on /dev/shm partition
    CIS Benchmark 1.1.2.2.3 - Ensure nosuid option set on /dev/shm partition
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.1.2.2.3',
        'name': 'Ensure nosuid option set on /dev/shm partition',
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
        
        # Check if nosuid option is present
        if mount_result.returncode == 0:
            mount_output = mount_result.stdout.strip()
            if 'nosuid' in mount_output:
                result['status'] = True
                result['details'] = '/dev/shm is mounted with nosuid option'
                logger.info('/dev/shm is mounted with nosuid option')
            else:
                result['status'] = False
                result['details'] = '/dev/shm is not mounted with nosuid option'
                logger.warning('/dev/shm is not mounted with nosuid option')
        else:
            result['status'] = False
            result['details'] = 'Could not retrieve /dev/shm mount information'
            logger.error('Could not retrieve /dev/shm mount information')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking /dev/shm nosuid option: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'devshm_nosuid': check_devshm_nosuid()
    }
    
    return results

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Direct execution for testing
    print(run())