import subprocess
import logging

logger = logging.getLogger(__name__)

def check_sctp_module() -> dict:
    """
    Check if sctp kernel module is available
    CIS Benchmark 3.2.4 - Ensure sctp kernel module is not available
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '3.2.4',
        'name': 'Ensure sctp kernel module is not available',
        'status': False,  # False means module is available (not compliant)
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check if module is loaded
        loaded_modules_cmd = "lsmod | grep sctp"
        loaded_modules_result = subprocess.run(
            loaded_modules_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if module is available in system modules
        available_modules_cmd = "modprobe -n -v sctp"
        available_modules_result = subprocess.run(
            available_modules_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # If either command returns output, the module is available
        if loaded_modules_result.stdout.strip() or available_modules_result.stdout.strip():
            result['status'] = False
            result['details'] = 'SCTP kernel module is available'
            logger.warning('SCTP kernel module is available')
        else:
            result['status'] = True
            result['details'] = 'SCTP kernel module is not available'
            logger.info('SCTP kernel module is not available')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking SCTP module: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'sctp_module': check_sctp_module()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())