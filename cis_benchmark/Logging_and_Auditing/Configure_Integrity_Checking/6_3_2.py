import subprocess
import logging

logger = logging.getLogger(__name__)

def check_filesystem_integrity_check():
    """
    Ensure filesystem integrity is regularly checked.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.3.2',
        'name': "Ensure filesystem integrity is regularly checked",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if AIDE cron job or systemd timer exists for regular checks
        process = subprocess.run(['systemctl', 'list-timers', 'aide.timer'], capture_output=True, text=True)
        if process.returncode == 0:
            result['status'] = True
            result['details'] = "Filesystem integrity is regularly checked via AIDE timer."
            logger.info(result['details'])
        else:
            result['details'] = "No systemd timer found for AIDE. Ensure a regular integrity check is configured."
            logger.error(result['details'])
    except Exception as e:
        result['details'] = f"Error checking filesystem integrity check: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'filesystem_integrity_checked': check_filesystem_integrity_check()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
