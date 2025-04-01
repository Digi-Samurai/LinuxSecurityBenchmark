import os
import logging

logger = logging.getLogger(__name__)

def check_world_writable_files():
    """
    Ensure world writable files and directories are secured.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '7.1.11',
        'name': "Ensure world writable files and directories are secured",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Search for world-writable files and directories
        for root, dirs, files in os.walk('/'):
            for name in dirs + files:
                path = os.path.join(root, name)
                if os.access(path, os.W_OK):  # Check if world-writable
                    result['details'] = f"Found world-writable file or directory: {path}"
                    logger.error(result['details'])
                    return result
        result['status'] = True
        result['details'] = "No world-writable files or directories found"
        logger.info(result['details'])
    except Exception as e:
        result['details'] = f"Error checking for world writable files: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'world_writable_files': check_world_writable_files()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
