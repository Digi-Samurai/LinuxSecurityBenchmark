import subprocess
import logging

logger = logging.getLogger(__name__)

def check_aide_installed():
    """
    Ensure AIDE is installed.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.3.1',
        'name': "Ensure AIDE is installed",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if AIDE is installed
        process = subprocess.run(['which', 'aide'], capture_output=True, text=True)
        if process.returncode == 0:
            result['status'] = True
            result['details'] = "AIDE is installed."
            logger.info(result['details'])
        else:
            result['details'] = "AIDE is not installed."
            logger.error(result['details'])
    except Exception as e:
        result['details'] = f"Error checking AIDE installation: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'aide_installed': check_aide_installed()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
