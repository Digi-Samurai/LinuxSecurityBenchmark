import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_audit_tools_owner() -> Dict[str, Any]:
    """
    Ensure audit tools owner is configured.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.4.9',
        'name': "Ensure audit tools owner is configured",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        audit_tools = ['/usr/sbin/auditctl', '/usr/sbin/audispd']  # Modify as needed
        correct_owner = 'root'

        for tool in audit_tools:
            if os.path.exists(tool):
                tool_owner = os.stat(tool).st_uid
                owner_name = os.getpwuid(tool_owner).pw_name
                if owner_name == correct_owner:
                    result['status'] = True
                    result['details'] = f"{tool} has the correct owner: {owner_name}."
                    logger.info(result['details'])
                else:
                    result['details'] = f"{tool} does not have the correct owner: {owner_name}."
                    logger.warning(result['details'])
            else:
                result['details'] = f"{tool} does not exist."
                logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking audit tools owner: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'audit_tools_owner': check_audit_tools_owner()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
