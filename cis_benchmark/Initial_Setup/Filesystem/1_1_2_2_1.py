import os
import subprocess
import logging

logger = logging.getLogger(__name__)

def check_devshm_separate_partition() -> dict:
    """
    Check if /dev/shm is a separate partition
    CIS Benchmark 1.1.2.2.1 - Ensure /dev/shm is a separate partition
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.1.2.2.1',
        'name': 'Ensure /dev/shm is a separate partition',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Use df to check if /dev/shm is a separate mount point
        df_cmd = "df -h /dev/shm"
        df_result = subprocess.run(
            df_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Use findmnt to get more detailed mount information
        findmnt_cmd = "findmnt -no FSTYPE /dev/shm"
        findmnt_result = subprocess.run(
            findmnt_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if the command was successful and shows a filesystem
        if (df_result.returncode == 0 and 
            findmnt_result.returncode == 0 and 
            findmnt_result.stdout.strip()):
            result['status'] = True
            result['details'] = '/dev/shm is a separate partition'
            logger.info('/dev/shm is a separate partition')
        else:
            result['status'] = False
            result['details'] = '/dev/shm is not a separate partition'
            logger.warning('/dev/shm is not a separate partition')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking /dev/shm partition: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'devshm_separate_partition': check_devshm_separate_partition()
    }
    
    return results

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Direct execution for testing
    print(run())