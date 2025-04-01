import os
import logging

logger = logging.getLogger(__name__)

def check_timesyncd_timeserver() -> dict:
    """
    Ensure systemd-timesyncd is configured with authorized timeserver
    CIS Benchmark 2.3.2.1
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.3.2.1',
        'name': 'Ensure systemd-timesyncd configured with authorized timeserver',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Path to systemd-timesyncd configuration
        timesyncd_config = '/etc/systemd/timesyncd.conf'
        
        # Authorized timeservers (you can modify this list)
        authorized_timeservers = [
            'time.google.com',
            'time.cloudflare.com',
            'pool.ntp.org',
            'ntp.ubuntu.com'
        ]
        
        # Check if configuration file exists
        if not os.path.exists(timesyncd_config):
            result['details'] = 'Timesyncd configuration file not found'
            logger.warning('Timesyncd configuration file not found')
            return result
        
        # Read configuration file
        with open(timesyncd_config, 'r') as f:
            config_content = f.read()
        
        # Check for NTP servers
        ntp_configured = False
        for server in authorized_timeservers:
            if server in config_content:
                ntp_configured = True
                break
        
        if ntp_configured:
            result['status'] = True
            result['details'] = 'Systemd-timesyncd configured with authorized timeserver'
            logger.info('Authorized timeserver found in configuration')
        else:
            result['details'] = 'No authorized timeserver found in configuration'
            logger.warning('No authorized timeserver configured')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking timesyncd configuration: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'timesyncd_timeserver': check_timesyncd_timeserver()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())