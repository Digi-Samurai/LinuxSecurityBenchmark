import logging
import subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_journald_compress_configured() -> Dict[str, Any]:
    """
    Ensure journald Compress is configured.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.1.2.3',
        'name': "Ensure journald Compress is configured",
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        # Check if Compress option is set in journald.conf
        config_check = subprocess.run(
            ["grep", "Compress", "/etc/systemd/journald.conf"],
            capture_output=True,
            text=True
        )
        
        if config_check.returncode == 0 and "yes" in config_check.stdout.lower():
            result['status'] = True
            result['details'] = "Journald compression is configured."
            logger.info(result['details'])
        else:
            result['details'] = "Journald compression is not configured."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking journald compression: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'journald_compress_configured': check_journald_compress_configured()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
