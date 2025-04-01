import subprocess
import logging

logger = logging.getLogger(__name__)

def check_nfs_services() -> dict:
    """
    Check if Network File System (NFS) services are not in use
    CIS Benchmark 2.1.9 - Ensure network file system services are not in use
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '2.1.9',
        'name': 'Ensure network file system services are not in use',
        'status': False,  # False means services are available (not compliant)
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Check if NFS services are installed or running
        nfs_services = [
            'nfs-kernel-server',  # Debian/Ubuntu
            'nfs-server',          # Red Hat/CentOS
            'rpc-server'
        ]
        
        # Check service status using systemctl
        systemctl_cmd = f"systemctl is-active {' '.join(nfs_services)}"
        systemctl_result = subprocess.run(
            systemctl_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check package installation
        package_check_cmd = f"dpkg -l {' '.join(nfs_services)} || rpm -q {' '.join(nfs_services)}"
        package_result = subprocess.run(
            package_check_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Determine if NFS services are in use
        if systemctl_result.returncode == 0 or package_result.returncode == 0:
            result['status'] = False
            result['details'] = 'NFS services are installed or running'
            logger.warning('NFS services are installed or running')
        else:
            result['status'] = True
            result['details'] = 'NFS services are not in use'
            logger.info('NFS services are not in use')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking NFS services: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'nfs_services': check_nfs_services()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())