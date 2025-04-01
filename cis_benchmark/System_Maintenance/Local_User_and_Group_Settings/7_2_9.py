import os
import logging

logger = logging.getLogger(__name__)

def check_local_interactive_user_home_dirs():
    """
    Ensure local interactive user home directories are configured.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '7.2.9',
        'name': "Ensure local interactive user home directories are configured",
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        with open('/etc/passwd', 'r') as passwd_file:
            for line in passwd_file:
                fields = line.split(':')
                username = fields[0]
                home_dir = fields[5]
                if home_dir and home_dir != '/nonexistent':  # Checking for valid home directories
                    if not os.path.exists(home_dir):
                        result['details'] = f"Home directory for user {username} does not exist: {home_dir}"
                        logger.error(result['details'])
                        return result
        result['status'] = True
        result['details'] = "All interactive users have valid home directories"
        logger.info(result['details'])
    except Exception as e:
        result['details'] = f"Error checking home directories: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'local_interactive_user_home_dirs_check': check_local_interactive_user_home_dirs()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
