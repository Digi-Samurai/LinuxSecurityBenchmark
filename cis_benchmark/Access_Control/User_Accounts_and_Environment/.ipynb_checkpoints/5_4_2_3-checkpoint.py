import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_root_gid_group() -> Dict[str, Any]:
    """
    Ensure the 'root' group is the only GID 0 group.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.4.2.3',
        'name': 'Ensure root group is the only GID 0 group',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        with open("/etc/group", "r") as f:
            gid_0_groups = [line.split(":")[0] for line in f if ":0:" in line]

        if gid_0_groups == ["root"]:
            result['status'] = True
            result['details'] = "Only 'root' group has GID 0."
            logger.info(result['details'])
        else:
            result['details'] = f"GID 0 groups found: {', '.join(gid_0_groups)}"
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking GID 0 groups: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'root_gid_group': check_root_gid_group()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
