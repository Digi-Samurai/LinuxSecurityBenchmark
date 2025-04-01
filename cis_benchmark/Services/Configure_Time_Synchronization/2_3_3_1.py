import os
import logging

logger = logging.getLogger(__name__)

def check_chrony_timeserver() -> dict:
    """
    Ensure chrony is configured with authorized timeserver
    CIS Benchmark 2.3.3.1
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.3.3.1',
        'name': 'Ensure chrony is configured with authorized timeserver',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Path to chrony configuration
        chrony_config = '/etc/chrony/chrony.conf'
        
        # Alternative config paths
        alternative_paths = [
            '/etc/chrony.conf',
            '/usr/local/etc/chrony.conf'
        ]
        
        # Authorized timeservers (you can modify this list)
        authorized_timeservers = [
            'time.google.com',
            'time.cloudflare.com',
            'pool.ntp.org',
            'ntp.ubuntu.com'
        ]
        
        # Find the actual config file
        config_file = None
        for path in [chrony_config] + alternative_paths:
            if os.path.exists(path):
                config_file = path
                break
        
        if not config_file:
            result['details'] = 'Chrony configuration file not found'
            logger.warning('Chrony configuration file not found')
            return result
        
        # Read configuration file
        with open(config_file, 'r') as f:
            config_content = f.read()
        
        # Check for NTP servers
        ntp_configured = False
        matching_servers = []
        
        for server in authorized_timeservers:
            if f'server {server}' in config_content:
                ntp_configured = True
                matching_servers.append(server)
        
        if ntp_configured:
            result['status'] = True
            result['details'] = f'Chrony configured with authorized timeserver(s): {", ".join(matching_servers)}'
            logger.info(f'Authorized timeserver(s) found: {matching_servers}')
        else:
            result['details'] = 'No authorized timeserver found in chrony configuration'
            logger.warning('No authorized timeserver configured for chrony')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking chrony configuration: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'chrony_timeserver': check_chrony_timeserver()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())