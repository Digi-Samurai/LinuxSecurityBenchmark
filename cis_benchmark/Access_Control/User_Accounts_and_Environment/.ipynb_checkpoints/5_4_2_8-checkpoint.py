import logging
import subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_locked_accounts() -> Dict[str, Any]:
    """
    Ensure accounts without a valid login shell are locked.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.4.2.8',
        'name': 'Ensure accounts without a valid login shell are locked',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        locked_accounts = []
        with open("/etc/passwd", "r") as f:
            for line in f:
                parts = line.strip().split(":")
                username, shell = parts[0], parts[-1]
                if shell in ["/usr/sbin/nologin", "/bin/false"]:
                    status = subprocess.getoutput(f"passwd -S {username}")
                    if " L " not in status:  # 'L' indicates locked
                        locked_accounts.append(username)

        if not locked_accounts:
            result['status'] = True
            result['details'] = "All non-login shell accounts are locked."
            logger.info(result['details'])
        else:
            result['details'] = f"Accounts with non-login shell but not locked: {', '.join(locked_accounts)}"
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking locked accounts: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'locked_accounts': check_locked_accounts()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
