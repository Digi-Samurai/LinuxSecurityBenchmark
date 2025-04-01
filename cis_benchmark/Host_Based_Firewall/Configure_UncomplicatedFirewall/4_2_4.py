import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_ufw_loopback_configuration() -> Dict[str, Any]:
    """
    Check UFW loopback traffic configuration
    CIS Benchmark 4.2.4 - Ensure ufw loopback traffic is configured
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '4.2.4',
        'name': 'Ensure ufw loopback traffic is configured',
        'status': False,  # False means not compliant
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check UFW loopback configuration using grep
        grep_cmd = "grep -P -- 'lo|127.0.0.0' /etc/ufw/before.rules"
        
        # Run the command
        grep_result = subprocess.run(
            grep_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if the grep command found any matches
        if grep_result.stdout.strip():
            # Found loopback-related rules
            result['status'] = True
            result['details'] = 'UFW loopback rules found in before.rules'
            logger.info(result['details'])
        else:
            # No loopback rules found
            result['details'] = 'No UFW loopback rules found in before.rules'
            logger.warning(result['details'])
        
        # Additional UFW status check
        try:
            ufw_status = subprocess.run(
                ['ufw', 'status'], 
                capture_output=True, 
                text=True
            )
            
            # Check if UFW is active
            if 'Status: active' in ufw_status.stdout:
                result['details'] += '. UFW is active'
            else:
                result['details'] += '. UFW is not active'
        except Exception as status_error:
            result['details'] += f'. Error checking UFW status: {status_error}'
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking UFW loopback configuration: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'ufw_loopback_configuration': check_ufw_loopback_configuration()
    }
    
    return results

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Direct execution for testing
    results = run()
    print(results['ufw_loopback_configuration'])