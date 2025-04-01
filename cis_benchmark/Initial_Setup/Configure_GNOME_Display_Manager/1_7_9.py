import os
import logging

logger = logging.getLogger(__name__)

GDM_LOCK_FILE = "/etc/dconf/db/gdm.d/locks/00-security-settings"

def check_gdm_autorun_never_override() -> dict:
    """
    Ensure GDM autorun-never setting is not overridden.
    CIS Benchmark 1.7.9 - Ensure GDM autorun-never is not overridden.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.7.9',
        'name': 'Ensure GDM autorun-never is not overridden',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        if os.path.exists(GDM_LOCK_FILE):
            with open(GDM_LOCK_FILE, 'r') as f:
                content = f.read()
                if "/org/gnome/desktop/media-handling/autorun-never" in content:
                    result['status'] = True
                    result['details'] = "GDM autorun-never is locked and cannot be overridden."
                    logger.info(result['details'])
                else:
                    result['details'] = "GDM autorun-never setting might be overridden."
                    logger.warning(result['details'])
        else:
            result['details'] = f"{GDM_LOCK_FILE} not found, settings might be unprotected."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking GDM autorun-never override: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'gdm_autorun_never_override': check_gdm_autorun_never_override()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
