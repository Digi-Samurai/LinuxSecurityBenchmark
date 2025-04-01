import subprocess
import logging

logger = logging.getLogger(__name__)

def check_rds_module() -> dict:
    """
    Check if rds kernel module is available
    CIS Benchmark 3.2.3 - Ensure rds kernel module is not available
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '3.2.3',
        'name': 'Ensure rds kernel module is not available',
        'status': False,  # False means module is available (not compliant)
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check if module is loaded
        loaded_modules_cmd = "lsmod | grep rds"
        loaded_modules_result = subprocess.run(
            loaded_modules_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if module is available in system modules
        available_modules_cmd = "modprobe -n -v rds"
        available_modules_result = subprocess.run(
            available_modules_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # If either command returns output, the module is available
        if loaded_modules_result.stdout.strip() or available_modules_result.stdout.strip():
            result['status'] = False
            result['details'] = 'RDS kernel module is available'
            logger.warning('RDS kernel module is available')
        else:
            result['status'] = True
            result['details'] = 'RDS kernel module is not available'
            logger.info('RDS kernel module is not available')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking RDS module: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'rds_module': check_rds_module()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())