import subprocess
import logging

# Setup logger
logger = logging.getLogger(__name__)

def check_ip6tables_default_deny() -> dict:
    """
    Check if ip6tables has a default deny policy
    CIS Benchmark 4.4.3.1 - Ensure ip6tables default deny firewall policy
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '4.4.3.1',
        'name': 'Ensure ip6tables default deny firewall policy',
        'status': False,
        'severity': 'high',
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
            result['details'] = "IPv6 is disabled, no ip6tables policy needed"
            logger.info("IPv6 is disabled, no ip6tables policy needed")
            return result
        
        # Check default policy for each chain (INPUT, OUTPUT, FORWARD)
        cmd = "ip6tables -L"
        ip6tables_output = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        if ip6tables_output.returncode != 0:
            result['status'] = False
            result['details'] = f"Error running ip6tables command: {ip6tables_output.stderr}"
            logger.error(result['details'])
            return result
        
        # Parse output to check default policies
        output_lines = ip6tables_output.stdout.splitlines()
        input_policy = ""
        forward_policy = ""
        output_policy = ""
        
        for line in output_lines:
            if line.startswith("Chain INPUT"):
                input_policy = line.split("policy ")[1].split()[0]
            elif line.startswith("Chain FORWARD"):
                forward_policy = line.split("policy ")[1].split()[0]
            elif line.startswith("Chain OUTPUT"):
                output_policy = line.split("policy ")[1].split()[0]
        
        # Check if all chains have a default DROP or REJECT policy
        if (input_policy in ["DROP", "REJECT"] and 
            forward_policy in ["DROP", "REJECT"] and 
            output_policy in ["DROP", "REJECT"]):
            
            result['status'] = True
            result['details'] = "Default deny policy is set on all ip6tables chains"
            logger.info("Default deny policy is set on all ip6tables chains")
        else:
            result['status'] = False
            result['details'] = (
                f"Default deny policy not set: INPUT={input_policy}, "
                f"FORWARD={forward_policy}, OUTPUT={output_policy}"
            )
            logger.warning(result['details'])
    
    except Exception as e:
        result['status'] = False
        result['details'] = f"Error checking ip6tables default policy: {e}"
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'ip6tables_default_deny': check_ip6tables_default_deny()
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