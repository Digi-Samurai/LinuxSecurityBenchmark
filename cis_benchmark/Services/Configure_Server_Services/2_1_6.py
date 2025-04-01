import subprocess
import logging

logger = logging.getLogger(__name__)

def check_ftp_service() -> dict:
    """
    Check if FTP server services are not in use
    CIS Benchmark 2.1.6 - Ensure ftp server services are not in use
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.1.6',
        'name': 'Ensure ftp server services are not in use',
        'status': True,  # Assume not running until proven otherwise
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check for vsftpd
        vsftpd_installed = subprocess.run(
            "which vsftpd", 
            shell=True, 
            capture_output=True, 
            text=True
        )
        vsftpd_active = subprocess.run(
            "systemctl is-active vsftpd", 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check for pure-ftpd
        pureftpd_installed = subprocess.run(
            "which pure-ftpd", 
            shell=True, 
            capture_output=True, 
            text=True
        )
        pureftpd_active = subprocess.run(
            "systemctl is-active pure-ftpd", 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # If any FTP server is found or active, it's not compliant
        if (vsftpd_installed.returncode == 0 or vsftpd_active.stdout.strip() == 'active' or
            pureftpd_installed.returncode == 0 or pureftpd_active.stdout.strip() == 'active'):
            result['status'] = False
            result['details'] = 'FTP server (vsftpd or pure-ftpd) is installed or running'
            logger.warning('FTP server service is in use')
        else:
            result['details'] = 'FTP server services are not in use'
            logger.info('FTP server services are not in use')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking FTP services: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'ftp_service': check_ftp_service()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())