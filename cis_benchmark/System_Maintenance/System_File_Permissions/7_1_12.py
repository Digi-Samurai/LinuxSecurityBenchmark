import os
import logging

logger = logging.getLogger(__name__)

def check_files_without_owner():
    """
    Ensure no files or directories without an owner and a group exist.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '7.1.12',
        'name': "Ensure no files or directories without an owner and a group exist",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Search for files and directories without an owner or group
        for root, dirs, files in os.walk('/'):
            for name in dirs + files:
                path = os.path.join(root, name)
                stat = os.stat(path)
                if stat.st_uid == 0 and stat.st_gid == 0:  # Check if no owner/group
                    result['details'] = f"File or directory without a valid owner/group: {path}"
                    logger.error(result['details'])
                    return result
        result['status'] = True
        result['details'] = "All files and directories have a valid owner and group"
        logger.info(result['details'])
    except Exception as e:
        result['details'] = f"Error checking for files without an owner/group: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'files_without_owner': check_files_without_owner()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
