import os
import logging

logger = logging.getLogger(__name__)

def check_gdm_auto_mount() -> dict:
    """
    Ensure GDM automatic mounting of removable media is disabled (Automated)

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.7.6',
        'name': 'Ensure GDM automatic mounting of removable media is disabled',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    config_path = "/etc/dconf/db/local.d/00-media-automount"

    try:
        if os.path.exists(config_path):
            with open(config_path, "r") as file:
                content = file.read()
                if "automount=false" in content and "automount-open=false" in content:
                    result['status'] = True
                    result['details'] = "GDM automatic mounting is disabled"
                    logger.info("GDM automatic mounting is disabled")
                else:
                    result['details'] = "GDM automatic mounting is not properly configured"
                    logger.warning("GDM automatic mounting is not properly configured")
        else:
            result['details'] = f"{config_path} file not found"
            logger.error(f"{config_path} file not found")

    except Exception as e:
        result['details'] = f"Error checking GDM auto mount: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'gdm_auto_mount': check_gdm_auto_mount()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
