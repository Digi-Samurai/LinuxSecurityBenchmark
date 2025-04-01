import os
import logging

logger = logging.getLogger(__name__)

def check_gdm_screen_lock() -> dict:
    """
    Ensure GDM screen locks when the user is idle (Automated)

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.7.4',
        'name': 'Ensure GDM screen locks when the user is idle',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    config_path = "/etc/dconf/db/local.d/00-screensaver"

    try:
        if os.path.exists(config_path):
            with open(config_path, "r") as file:
                content = file.read()
                if "idle-delay=uint32 900" in content:
                    result['status'] = True
                    result['details'] = "GDM screen lock is enabled"
                    logger.info("GDM screen lock is enabled")
                else:
                    result['details'] = "GDM screen lock is not properly configured"
                    logger.warning("GDM screen lock is not properly configured")
        else:
            result['details'] = f"{config_path} file not found"
            logger.error(f"{config_path} file not found")

    except Exception as e:
        result['details'] = f"Error checking GDM screen lock: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'gdm_screen_lock': check_gdm_screen_lock()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
