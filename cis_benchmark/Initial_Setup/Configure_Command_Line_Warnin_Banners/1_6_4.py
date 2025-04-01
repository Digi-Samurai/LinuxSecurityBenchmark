import os
import stat
import logging

logger = logging.getLogger(__name__)

MOTD_PATH = "/etc/motd"

def check_motd_permissions() -> dict:
    """
    Ensure /etc/motd permissions are set properly.
    CIS Benchmark 1.6.4 - Ensure access to /etc/motd is restricted.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.6.4',
        'name': 'Ensure access to /etc/motd is configured',
        'status': False,
        'severity': 'low',
        'details': ''
    }

    try:
        if os.path.exists(MOTD_PATH):
            file_stat = os.stat(MOTD_PATH)
            mode = stat.S_IMODE(file_stat.st_mode)

            if mode & stat.S_IWOTH == 0 and mode & stat.S_IROTH == 0:  # Not world-writable or world-readable
                result['status'] = True
                result['details'] = "Permissions on /etc/motd are correctly configured."
                logger.info(result['details'])
            else:
                result['details'] = "Permissions on /etc/motd are too permissive."
                logger.warning(result['details'])
        else:
            result['details'] = "/etc/motd does not exist."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking /etc/motd permissions: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'motd_permissions': check_motd_permissions()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
