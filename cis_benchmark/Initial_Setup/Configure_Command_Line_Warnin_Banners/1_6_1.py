import os
import logging

logger = logging.getLogger(__name__)

MOTD_PATH = "/etc/motd"

def check_motd() -> dict:
    """
    Ensure message of the day (MOTD) is configured properly.
    CIS Benchmark 1.6.1 - Ensure MOTD does not contain sensitive information.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.6.1',
        'name': 'Ensure MOTD is configured properly',
        'status': False,
        'severity': 'low',
        'details': ''
    }

    try:
        if os.path.exists(MOTD_PATH):
            with open(MOTD_PATH, 'r') as f:
                content = f.read()
            
            if "unauthorized" in content.lower() or "access" in content.lower():
                result['status'] = True
                result['details'] = "MOTD is configured with a proper warning."
                logger.info(result['details'])
            else:
                result['details'] = "MOTD does not contain a proper warning message."
                logger.warning(result['details'])
        else:
            result['details'] = "MOTD file does not exist."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking MOTD: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'motd_configured': check_motd()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
