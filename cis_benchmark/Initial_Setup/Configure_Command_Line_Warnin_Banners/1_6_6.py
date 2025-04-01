import os
import stat
import logging

logger = logging.getLogger(__name__)

ISSUE_NET_PATH = "/etc/issue.net"

def check_issue_net_permissions() -> dict:
    """
    Ensure /etc/issue.net permissions are set properly.
    CIS Benchmark 1.6.6 - Ensure access to /etc/issue.net is restricted.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.6.6',
        'name': 'Ensure access to /etc/issue.net is configured',
        'status': False,
        'severity': 'low',
        'details': ''
    }

    try:
        if os.path.exists(ISSUE_NET_PATH):
            file_stat = os.stat(ISSUE_NET_PATH)
            mode = stat.S_IMODE(file_stat.st_mode)

            if mode & stat.S_IWOTH == 0 and mode & stat.S_IROTH == 0:  # Not world-writable or world-readable
                result['status'] = True
                result['details'] = "Permissions on /etc/issue.net are correctly configured."
                logger.info(result['details'])
            else:
                result['details'] = "Permissions on /etc/issue.net are too permissive."
                logger.warning(result['details'])
        else:
            result['details'] = "/etc/issue.net does not exist."
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking /etc/issue.net permissions: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'issue_net_permissions': check_issue_net_permissions()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
