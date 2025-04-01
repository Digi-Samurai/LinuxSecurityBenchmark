import subprocess
import logging

logger = logging.getLogger(__name__)

def check_unused_filesystem_modules() -> dict:
    """
    Check for unused filesystem kernel modules
    CIS Benchmark 1.1.1.10 - Ensure unused filesystem kernel modules are not available
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.1.1.10',
        'name': 'Ensure unused filesystem kernel modules are not available',
        'status': True,
        'severity': 'medium',
        'details': '',
        'unused_modules': []
    }
    
    # List of filesystem modules typically considered unused
    unused_modules = [
        'afs', 'ceph', 'cifs', 'exfat', 'fat', 'fscache', 
        'fuse', 'gfs2'
    ]
    
    try:
        # Check each module's availability
        for module in unused_modules:
            # Check if module is loaded
            loaded_modules_cmd = f"lsmod | grep {module}"
            loaded_modules_result = subprocess.run(
                loaded_modules_cmd, 
                shell=True, 
                capture_output=True, 
                text=True
            )
            
            # Check if module is available in system modules
            available_modules_cmd = f"modprobe -n -v {module}"
            available_modules_result = subprocess.run(
                available_modules_cmd, 
                shell=True, 
                capture_output=True, 
                text=True
            )
            
            # If either command returns output, the module is available
            if loaded_modules_result.stdout.strip() or available_modules_result.stdout.strip():
                result['status'] = False
                result['unused_modules'].append(module)
        
        # Update details based on findings
        if not result['status']:
            result['details'] = f"Unused modules found: {', '.join(result['unused_modules'])}"
            logger.warning(f"Unused filesystem modules available: {result['unused_modules']}")
        else:
            result['details'] = 'No unused filesystem modules found'
            logger.info('No unused filesystem modules are available')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking unused filesystem modules: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'unused_filesystem_modules': check_unused_filesystem_modules()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())