import subprocess
import logging
import os

logger = logging.getLogger(__name__)

def check_package_manager_repos() -> dict:
    """
    Check if package manager repositories are properly configured
    CIS Benchmark 1.2.1.2 - Ensure package manager repositories are configured

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.2.1.2',
        'name': 'Ensure package manager repositories are configured',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        if is_debian():
            repo_files = ["/etc/apt/sources.list"] + get_files_from_dir("/etc/apt/sources.list.d/")
            repo_cmd = "grep -E '^deb ' " + " ".join(repo_files)
        elif is_rhel():
            repo_cmd = "yum repolist --enabled"
        else:
            result['details'] = 'Unsupported OS for this check'
            return result

        repo_result = subprocess.run(repo_cmd, shell=True, capture_output=True, text=True)

        if repo_result.returncode == 0 and repo_result.stdout.strip():
            result['status'] = True
            result['details'] = 'Package manager repositories are configured correctly'
            logger.info(result['details'])
        else:
            result['details'] = 'No valid package repositories found'
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f'Error checking package repositories: {e}'
        logger.error(result['details'])

    return result

def is_debian():
    """Detect if the system is Debian-based"""
    try:
        return subprocess.run("which apt", shell=True, capture_output=True).returncode == 0
    except:
        return False

def is_rhel():
    """Detect if the system is RHEL-based"""
    try:
        return subprocess.run("which yum", shell=True, capture_output=True).returncode == 0
    except:
        return False

def get_files_from_dir(directory):
    """Get a list of files from a directory if it exists"""
    return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))] if os.path.exists(directory) else []

def run():
    return {'package_manager_repos_configured': check_package_manager_repos()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
