import os
import stat
import logging

logger = logging.getLogger(__name__)

ISSUE_PATH = "/etc/issue"

def check_issue_permissions() -> dict:
    """
    Ensure /etc/issue permissions are set properly.
    CIS Benchmark 1.6.5 - Ensure access to /etc/issue is restricted.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.6.5',
        'name': 'Ensure access to /etc/issue is configured',
        'status': False,
        'severity': 'low',
        'details': ''
    }

    try:
        if os.path.exists(ISSUE_PATH):
            file_stat = os.stat(ISSUE_PATH)
            mode = stat.S_IMODE(file_stat.st_mode)

            if mode & stat.S_IWOTH == 0 and mode & stat.S_IROTH == 0:  # Not world-writable or world-readable
                result['status'] = True
                result['details'] = "Permissions on /etc/issue are correctly configured."
                logger.info(result['details'])
            else:
                result['details'] = "Permissions on /etc/issue are too permissive."
                logger.warning(result['details'])
        else:
            result['details'] = "/etc/issue does not exist."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking /etc/issue permissions: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'issue_permissions': check_issue_permissions()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
