import os
import logging

logger = logging.getLogger(__name__)

def check_dot_files_access():
    """
    Ensure local interactive user dot files access is configured.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '7.2.10',
        'name': "Ensure local interactive user dot files access is configured",
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        dot_files = ['.bashrc', '.bash_profile', '.profile', '.bash_logout', '.vimrc']
        for dot_file in dot_files:
            for dirpath, dirnames, filenames in os.walk('/home'):
                for filename in filenames:
                    if filename == dot_file:
                        file_path = os.path.join(dirpath, filename)
                        if os.access(file_path, os.R_OK | os.W_OK | os.X_OK):
                            logger.info(f"Dot file {file_path} is accessible")
                        else:
                            result['details'] = f"Dot file {file_path} is not accessible"
                            logger.error(result['details'])
                            return result
        result['status'] = True
        result['details'] = "All local interactive user dot files are configured with appropriate access"
        logger.info(result['details'])
    except Exception as e:
        result['details'] = f"Error checking dot files access: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'dot_files_access_check': check_dot_files_access()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
