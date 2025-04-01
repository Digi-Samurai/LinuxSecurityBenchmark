import subprocess
import logging

# Setup logger
logger = logging.getLogger(__name__)

def check_ip6tables_loopback() -> dict:
    """
    Check if ip6tables loopback traffic is correctly configured
    CIS Benchmark 4.4.3.2 - Ensure ip6tables loopback traffic is configured
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '4.4.3.2',
        'name': 'Ensure ip6tables loopback traffic is configured',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # First check if IPv6 is enabled
        ipv6_check = "sysctl -n net.ipv6.conf.all.disable_ipv6"
        ipv6_check_output = subprocess.run(
            ipv6_check, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # If IPv6 is disabled, this check is not applicable
        if ipv6_check_output.stdout.strip() == "1":
            result['status'] = True
            result['details'] = "IPv6 is disabled, no ip6tables loopback configuration needed"
            logger.info("IPv6 is disabled, no ip6tables loopback configuration needed")
            return result
        
        # Check loopback allow rule
        lo_allow_cmd = "ip6tables -L INPUT -v | grep -E '::1/128|lo'"
        lo_allow_output = subprocess.run(
            lo_allow_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check loopback interfaces block rule
        lo_block_cmd = "ip6tables -L INPUT -v | grep '! lo' | grep DROP"
        lo_block_output = subprocess.run(
            lo_block_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Both conditions must be met
        if lo_allow_output.stdout.strip() and lo_block_output.stdout.strip():
            result['status'] = True
            result['details'] = "IPv6 loopback traffic is properly configured in ip6tables"
            logger.info("IPv6 loopback traffic is properly configured in ip6tables")
        else:
            result['status'] = False
            missing = []
            if not lo_allow_output.stdout.strip():
                missing.append("Allow rule for loopback interface")
            if not lo_block_output.stdout.strip():
                missing.append("Block rule for non-loopback traffic on loopback interface")
            
            result['details'] = f"Missing ip6tables loopback configuration: {', '.join(missing)}"
            logger.warning(result['details'])
    
    except Exception as e:
        result['status'] = False
        result['details'] = f"Error checking ip6tables loopback configuration: {e}"
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'ip6tables_loopback': check_ip6tables_loopback()
    }
    
    return results

if __name__ == '__main__':
    # Configure logging for direct execution
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Direct execution for testing
    print(run())