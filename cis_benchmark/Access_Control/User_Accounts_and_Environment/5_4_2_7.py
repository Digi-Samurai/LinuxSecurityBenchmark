import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_system_accounts_shells() -> Dict[str, Any]:
    """
    Ensure system accounts do not have a valid login shell.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.4.2.7',
        'name': 'Ensure system accounts do not have a valid login shell',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        system_accounts = []
        with open("/etc/passwd", "r") as f:
            for line in f:
                parts = line.strip().split(":")
                username, uid, shell = parts[0], int(parts[2]), parts[-1]
                if uid >= 1000 or username in ["root"]:
                    continue
                if shell not in ["/usr/sbin/nologin", "/bin/false"]:
                    system_accounts.append(username)

        if not system_accounts:
            result['status'] = True
            result['details'] = "All system accounts have a non-login shell."
            logger.info(result['details'])
        else:
            result['details'] = f"System accounts with login shells: {', '.join(system_accounts)}"
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking system accounts: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'system_accounts_shells': check_system_accounts_shells()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
