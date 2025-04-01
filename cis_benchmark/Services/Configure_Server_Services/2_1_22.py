import subprocess
import logging
import json

logger = logging.getLogger(__name__)

def check_network_services() -> dict:
    """
    Check network services listening on interfaces
    CIS Benchmark 2.1.22 - Ensure only approved services are listening on a network interface
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.1.22',
        'name': 'Ensure only approved services are listening on a network interface',
        'status': None,  # Manual check, so status is None
        'severity': 'high',
        'details': ''
    }
    
    try:
        # Get all listening network services
        listening_services_cmd = (
            "ss -tuln | awk 'NR>1 {print $1 \" \" $4 \" \" $5}' | "
            "jq -Rn '[inputs | split(\" \") | select(length > 0)] | unique'"
        )
        
        listening_services_result = subprocess.run(
            listening_services_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Approved services (this list should be customized)
        approved_services = [
            '22',     # SSH
            '25',     # SMTP
            '53',     # DNS
            '80',     # HTTP
            '123',    # NTP
            '443',    # HTTPS
        ]
        
        # Parse the listening services
        try:
            services = json.loads(listening_services_result.stdout)
        except json.JSONDecodeError:
            services = []
        
        # Check each service
        unapproved_services = []
        for service in services:
            # Extract port number
            try:
                port = service[-1].split(':')[-1]
                if port not in approved_services:
                    unapproved_services.append(service)
            except (IndexError, ValueError):
                pass
        
        # Prepare result details
        if unapproved_services:
            result['details'] = (
                "MANUAL CHECK REQUIRED: Unapproved services detected\n"
                f"Unapproved services: {json.dumps(unapproved_services, indent=2)}\n"
                "Review and confirm each service's purpose and necessity"
            )
            logger.warning("Unapproved network services detected")
        else:
            result['details'] = "No unapproved network services detected"
            logger.info("No unapproved network services found")
    
    except Exception as e:
        result['details'] = f'Error checking network services: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'network_services': check_network_services()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())