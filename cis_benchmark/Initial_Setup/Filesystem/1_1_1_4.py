import subprocess
import logging

logger = logging.getLogger(__name__)

def check_hfsplus_module() -> dict:
    """
    Check if hfsplus kernel module is available
    CIS Benchmark 1.1.1.4 - Ensure hfsplus kernel module is not available
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.1.1.4',
        'name': 'Ensure hfsplus kernel module is not available',
        'status': False,  # False means module is available (not compliant)
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check if module is loaded
        loaded_modules_cmd = "lsmod | grep hfsplus"
        loaded_modules_result = subprocess.run(
            loaded_modules_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if module is available in system modules
        available_modules_cmd = "modprobe -n -v hfsplus"
        available_modules_result = subprocess.run(
            available_modules_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # If either command returns output, the module is available
        if loaded_modules_result.stdout.strip() or available_modules_result.stdout.strip():
            result['status'] = False
            result['details'] = 'HFS+ kernel module is available'
            logger.warning('HFS+ kernel module is available')
        else:
            result['status'] = True
            result['details'] = 'HFS+ kernel module is not available'
            logger.info('HFS+ kernel module is not available')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking hfsplus module: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'hfsplus_module': check_hfsplus_module()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())