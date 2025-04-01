import os
import logging

logger = logging.getLogger(__name__)

GDM_CONFIG = "/etc/dconf/db/gdm.d/00-security-settings"

def check_gdm_removable_media() -> dict:
    """
    Ensure GDM does not allow automatic mounting of removable media.
    CIS Benchmark 1.7.7 - Ensure disabling automatic mounting of removable media is not overridden.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.7.7',
        'name': 'Ensure GDM disabling automatic mounting of removable media is not overridden',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        if os.path.exists(GDM_CONFIG):
            with open(GDM_CONFIG, 'r') as f:
                content = f.read()
                if "automount=false" in content:
                    result['status'] = True
                    result['details'] = "GDM is correctly configured to disable automatic mounting of removable media."
                    logger.info(result['details'])
                else:
                    result['details'] = "GDM automatic mounting of removable media is not disabled."
                    logger.warning(result['details'])
        else:
            result['details'] = f"{GDM_CONFIG} not found, configuration might be missing."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking GDM removable media settings: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'gdm_removable_media': check_gdm_removable_media()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
