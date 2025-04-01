import subprocess
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_icmp_redirects() -> Dict[str, Any]:
    """
    Check if ICMP redirects are not accepted
    CIS Benchmark 3.3.5 - Ensure ICMP redirects are not accepted
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '3.3.5',
        'name': 'Ensure ICMP redirects are not accepted',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check ICMP redirects for all and default interfaces
        all_redirects_cmd = "sysctl net.ipv4.conf.all.accept_redirects"
        default_redirects_cmd = "sysctl net.ipv4.conf.default.accept_redirects"
        
        all_result = subprocess.run(
            all_redirects_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        default_result = subprocess.run(
            default_redirects_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # IPv6 check
        ipv6_all_redirects_cmd = "sysctl net.ipv6.conf.all.accept_redirects"
        ipv6_default_redirects_cmd = "sysctl net.ipv6.conf.default.accept_redirects"
        
        ipv6_all_result = subprocess.run(
            ipv6_all_redirects_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        ipv6_default_result = subprocess.run(
            ipv6_default_redirects_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if redirects are disabled (should be 0)
        ipv4_all_disabled = "net.ipv4.conf.all.accept_redirects = 0" in all_result.stdout
        ipv4_default_disabled = "net.ipv4.conf.default.accept_redirects = 0" in default_result.stdout
        ipv6_all_disabled = "net.ipv6.conf.all.accept_redirects = 0" in ipv6_all_result.stdout
        ipv6_default_disabled = "net.ipv6.conf.default.accept_redirects = 0" in ipv6_default_result.stdout
        
        if (ipv4_all_disabled and ipv4_default_disabled and 
            ipv6_all_disabled and ipv6_default_disabled):
            result['status'] = True
            result['details'] = 'ICMP redirects are disabled for all interfaces (IPv4 and IPv6)'
            logger.info(result['details'])
        else:
            result['details'] = 'ICMP redirects are enabled'
            logger.warning(result['details'])
            
            # Provide more specific information
            if not ipv4_all_disabled:
                result['details'] += '. IPv4 all interfaces accept redirects'
            if not ipv4_default_disabled:
                result['details'] += '. IPv4 default interface accepts redirects'
            if not ipv6_all_disabled:
                result['details'] += '. IPv6 all interfaces accept redirects'
            if not ipv6_default_disabled:
                result['details'] += '. IPv6 default interface accepts redirects'
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking ICMP redirects: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'icmp_redirects': check_icmp_redirects()
    }
    
    return results

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Direct execution for testing
    results = run()
    print(results['icmp_redirects'])