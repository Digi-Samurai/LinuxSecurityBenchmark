import subprocess
import logging
import re

# Setup logger
logger = logging.getLogger(__name__)

def check_ip6tables_open_ports() -> dict:
    """
    Check if ip6tables rules exist for all open ports
    CIS Benchmark 4.4.3.4 - Ensure ip6tables firewall rules exist for all open ports
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '4.4.3.4',
        'name': 'Ensure ip6tables firewall rules exist for all open ports',
        'status': False,
        'severity': 'high',
        'details': '',
        'open_ports': [],
        'unprotected_ports': []
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
            result['details'] = "IPv6 is disabled, no ip6tables rules needed"
            logger.info("IPv6 is disabled, no ip6tables rules needed")
            return result
        
        # Get list of listening TCP6 ports
        tcp6_ports_cmd = "ss -6tuln | grep LISTEN | awk '{print $5}' | awk -F':' '{print $NF}'"
        tcp6_ports_output = subprocess.run(
            tcp6_ports_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Get list of listening UDP6 ports
        udp6_ports_cmd = "ss -6tuln | grep UDP | awk '{print $5}' | awk -F':' '{print $NF}'"
        udp6_ports_output = subprocess.run(
            udp6_ports_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Get ip6tables rules
        ip6tables_rules_cmd = "ip6tables -L INPUT -v -n"
        ip6tables_rules_output = subprocess.run(
            ip6tables_rules_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Parse open ports
        open_ports = []
        for line in tcp6_ports_output.stdout.strip().splitlines():
            if line and line.isdigit():
                open_ports.append((line, 'tcp6'))
        
        for line in udp6_ports_output.stdout.strip().splitlines():
            if line and line.isdigit():
                open_ports.append((line, 'udp6'))
        
        # Parse ip6tables rules
        rules = ip6tables_rules_output.stdout.strip()
        
        # Check if each open port has a corresponding rule
        unprotected_ports = []
        
        for port, proto in open_ports:
            port_pattern = f"dpt:{port}"
            proto_pattern = proto.upper()
            
            # Check if rule exists for this port
            if not re.search(port_pattern, rules) or not re.search(proto_pattern, rules):
                unprotected_ports.append(f"{port}/{proto}")
        
        # Set result
        result['open_ports'] = [f"{port}/{proto}" for port, proto in open_ports]
        result['unprotected_ports'] = unprotected_ports
        
        if unprotected_ports:
            result['status'] = False
            result['details'] = f"Missing IPv6 firewall rules for ports: {', '.join(unprotected_ports)}"
            logger.warning(result['details'])
        else:
            result['status'] = True
            result['details'] = "All open IPv6 ports have corresponding firewall rules"
            logger.info("All open IPv6 ports have corresponding firewall rules")
    
    except Exception as e:
        result['status'] = False
        result['details'] = f"Error checking ip6tables rules for open ports: {e}"
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'ip6tables_open_ports': check_ip6tables_open_ports()
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