import os
import logging

logger = logging.getLogger(__name__)

def check_gdm_screen_lock_override() -> dict:
    """
    Ensure GDM screen locks cannot be overridden (Automated)

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.7.5',
        'name': 'Ensure GDM screen locks cannot be overridden',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    lockdown_path = "/etc/dconf/db/local.d/locks/screensaver"

    try:
        if os.path.exists(lockdown_path):
            with open(lockdown_path, "r") as file:
                content = file.read()
                if "org/gnome/desktop/session/idle-delay" in content:
                    result['status'] = True
                    result['details'] = "GDM screen lock override is disabled"
                    logger.info("GDM screen lock override is disabled")
                else:
                    result['details'] = "GDM screen lock override is not properly configured"
                    logger.warning("GDM screen lock override is not properly configured")
        else:
            result['details'] = f"{lockdown_path} file not found"
            logger.error(f"{lockdown_path} file not found")

    except Exception as e:
        result['details'] = f"Error checking GDM screen lock override: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'gdm_screen_lock_override': check_gdm_screen_lock_override()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
