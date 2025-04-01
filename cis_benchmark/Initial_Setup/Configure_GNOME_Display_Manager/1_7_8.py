import os
import logging

logger = logging.getLogger(__name__)

GDM_CONFIG = "/etc/dconf/db/gdm.d/00-security-settings"

def check_gdm_autorun_never() -> dict:
    """
    Ensure GDM autorun-never is enabled.
    CIS Benchmark 1.7.8 - Ensure GDM autorun-never is enabled.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.7.8',
        'name': 'Ensure GDM autorun-never is enabled',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        if os.path.exists(GDM_CONFIG):
            with open(GDM_CONFIG, 'r') as f:
                content = f.read()
                if "autorun-never=true" in content:
                    result['status'] = True
                    result['details'] = "GDM autorun-never is correctly enabled."
                    logger.info(result['details'])
                else:
                    result['details'] = "GDM autorun-never is not enabled."
                    logger.warning(result['details'])
        else:
            result['details'] = f"{GDM_CONFIG} not found, configuration might be missing."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking GDM autorun-never setting: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'gdm_autorun_never': check_gdm_autorun_never()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
