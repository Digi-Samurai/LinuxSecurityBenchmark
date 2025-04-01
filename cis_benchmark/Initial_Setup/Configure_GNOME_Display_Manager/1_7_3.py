import os
import logging

logger = logging.getLogger(__name__)

def check_gdm_disable_user_list() -> dict:
    """
    Ensure GDM disable-user-list option is enabled (Automated)
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.7.3',
        'name': 'Ensure GDM disable-user-list option is enabled',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    config_path = "/etc/gdm3/greeter.dconf-defaults"

    try:
        if os.path.exists(config_path):
            with open(config_path, "r") as file:
                content = file.read()
                if "disable-user-list=true" in content:
                    result['status'] = True
                    result['details'] = "GDM user list is disabled"
                    logger.info("GDM user list is disabled")
                else:
                    result['details'] = "GDM user list is not disabled"
                    logger.warning("GDM user list is not disabled")
        else:
            result['details'] = f"{config_path} file not found"
            logger.error(f"{config_path} file not found")

    except Exception as e:
        result['details'] = f"Error checking GDM disable-user-list: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'gdm_disable_user_list': check_gdm_disable_user_list()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
