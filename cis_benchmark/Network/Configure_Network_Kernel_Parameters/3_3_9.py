import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_suspicious_packets_logging() -> Dict[str, Any]:
    """
    Check if suspicious packets are logged
    CIS Benchmark 3.3.9 - Ensure suspicious packets are logged
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '3.3.9',
        'name': 'Ensure suspicious packets are logged',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check log martians settings
        all_log_martians_cmd = "sysctl net.ipv4.conf.all.log_martians"
        default_log_martians_cmd = "sysctl net.ipv4.conf.default.log_martians"
        
        all_log_martians = subprocess.run(
            all_log_martians_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        default_log_martians = subprocess.run(
            default_log_martians_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if both are set to 1 (enabled)
        if (all_log_martians.stdout.strip() == "net.ipv4.conf.all.log_martians = 1" and
            default_log_martians.stdout.strip() == "net.ipv4.conf.default.log_martians = 1"):
            result['status'] = True
            result['details'] = 'Suspicious packets logging is enabled on all and default interfaces'
            logger.info(result['details'])
        else:
            result['details'] = 'Suspicious packets logging is not fully enabled'
            logger.warning(result['details'])
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking suspicious packets logging: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'suspicious_packets_logging': check_suspicious_packets_logging()
    }
    
    return results

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())