import os
import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_at_daemon_restrictions() -> Dict[str, Any]:
    """
    Check restrictions on at daemon for authorized users
    CIS Benchmark 2.4.2.1 - Ensure at is restricted to authorized users
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.4.2.1',
        'name': 'Ensure at is restricted to authorized users',
        'status': False,  # False means not compliant
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check at.allow and at.deny files
        at_allow_path = '/etc/at.allow'
        at_deny_path = '/etc/at.deny'
        
        # Preferred configuration: at.allow exists and at.deny does not
        if os.path.exists(at_allow_path) and not os.path.exists(at_deny_path):
            # Check at.allow permissions
            at_allow_stat = os.stat(at_allow_path)
            
            # Verify permissions (should be 644 or more restrictive)
            if at_allow_stat.st_mode & 0o777 == 0o644:
                # Check file ownership (should be root:root)
                if at_allow_stat.st_uid == 0 and at_allow_stat.st_gid == 0:
                    result['status'] = True
                    result['details'] = 'at.allow exists with correct permissions and ownership'
                else:
                    result['details'] = 'at.allow does not have root ownership'
            else:
                result['details'] = f'at.allow has incorrect permissions: {oct(at_allow_stat.st_mode & 0o777)}'
        
        elif not os.path.exists(at_allow_path) and os.path.exists(at_deny_path):
            # If at.allow doesn't exist, at.deny should be empty
            with open(at_deny_path, 'r') as f:
                if len(f.read().strip()) == 0:
                    result['status'] = True
                    result['details'] = 'at.deny exists but is empty'
                else:
                    result['details'] = 'at.deny is not empty'
        else:
            result['details'] = 'Incorrect at daemon configuration'
        
        # Additional verification using at command
        try:
            # Check if at daemon is configured
            subprocess.run(['which', 'at'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Try to get at daemon status
            at_status = subprocess.run(
                ['systemctl', 'is-enabled', 'atd'], 
                capture_output=True, 
                text=True
            )
            
            if at_status.returncode == 0 and 'enabled' in at_status.stdout:
                result['details'] += '. atd service is enabled'
        except subprocess.CalledProcessError:
            # at command not found or service not managed by systemctl
            result['details'] += '. Unable to verify at daemon status'
        
        # Log the result
        if result['status']:
            logger.info(result['details'])
        else:
            logger.warning(result['details'])
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking at daemon restrictions: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'at_daemon_restrictions': check_at_daemon_restrictions()
    }
    
    return results

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Direct execution for testing
    results = run()
    print(results['at_daemon_restrictions'])