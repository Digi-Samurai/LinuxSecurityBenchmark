import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_audit_tools_group_owner() -> Dict[str, Any]:
    """
    Ensure audit tools group owner is configured.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.4.10',
        'name': "Ensure audit tools group owner is configured",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        audit_tools = ['/usr/sbin/auditctl', '/usr/sbin/audispd']  # Modify as needed
        correct_group = 'root'

        for tool in audit_tools:
            if os.path.exists(tool):
                tool_group = os.stat(tool).st_gid
                group_name = os.getgrgid(tool_group).gr_name
                if group_name == correct_group:
                    result['status'] = True
                    result['details'] = f"{tool} has the correct group owner: {group_name}."
                    logger.info(result['details'])
                else:
                    result['details'] = f"{tool} does not have the correct group owner: {group_name}."
                    logger.warning(result['details'])
            else:
                result['details'] = f"{tool} does not exist."
                logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking audit tools group owner: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'audit_tools_group_owner': check_audit_tools_group_owner()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
