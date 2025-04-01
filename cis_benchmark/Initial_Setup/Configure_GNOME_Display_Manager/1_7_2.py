import os
import logging

logger = logging.getLogger(__name__)

def check_gdm_login_banner() -> dict:
    """
    Ensure GDM login banner is configured (Automated)
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.7.2',
        'name': 'Ensure GDM login banner is configured',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    banner_path = "/etc/gdm3/greeter.dconf-defaults"
    
    try:
        if os.path.exists(banner_path):
            with open(banner_path, "r") as file:
                content = file.read()
                if "banner-message-enable=true" in content:
                    result['status'] = True
                    result['details'] = "GDM login banner is enabled"
                    logger.info("GDM login banner is enabled")
                else:
                    result['details'] = "GDM login banner is not properly configured"
                    logger.warning("GDM login banner is not properly configured")
        else:
            result['details'] = f"{banner_path} file not found"
            logger.error(f"{banner_path} file not found")
    
    except Exception as e:
        result['details'] = f"Error checking GDM login banner: {e}"
        logger.error(result['details'])
    
    return result

def run():
    return {'gdm_login_banner': check_gdm_login_banner()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
