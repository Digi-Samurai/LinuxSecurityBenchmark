import subprocess
import logging

logger = logging.getLogger(__name__)

def check_cramfs_module() -> dict:
    """
    Check if cramfs kernel module is available
    CIS Benchmark 1.1.1.1 - Ensure cramfs kernel module is not available
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.1.1.1',
        'name': 'Ensure cramfs kernel module is not available',
        'status': False,  # False means module is available (not compliant)
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check if module is loaded
        loaded_modules_cmd = "lsmod | grep cramfs"
        loaded_modules_result = subprocess.run(
            loaded_modules_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if module is available in system modules
        available_modules_cmd = "modprobe -n -v cramfs"
        available_modules_result = subprocess.run(
            available_modules_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # If either command returns output, the module is available
        if loaded_modules_result.stdout.strip() or available_modules_result.stdout.strip():
            result['status'] = False
            result['details'] = 'Cramfs kernel module is available'
            logger.warning('Cramfs kernel module is available')
        else:
            result['status'] = True
            result['details'] = 'Cramfs kernel module is not available'
            logger.info('Cramfs kernel module is not available')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking cramfs module: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'cramfs_module': check_cramfs_module()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())