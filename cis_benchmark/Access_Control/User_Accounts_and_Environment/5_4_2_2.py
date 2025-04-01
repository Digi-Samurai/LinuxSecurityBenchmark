import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_root_gid_account() -> Dict[str, Any]:
    """
    Ensure root is the only GID 0 account.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.4.2.2',
        'name': 'Ensure root is the only GID 0 account',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        with open("/etc/passwd", "r") as f:
            gid_0_accounts = [line.split(":")[0] for line in f if ":0:" in line.split(":")[3]]

        if gid_0_accounts == ["root"]:
            result['status'] = True
            result['details'] = "Only 'root' has GID 0."
            logger.info(result['details'])
        else:
            result['details'] = f"GID 0 accounts found: {', '.join(gid_0_accounts)}"
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking GID 0 accounts: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'root_gid_account': check_root_gid_account()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
