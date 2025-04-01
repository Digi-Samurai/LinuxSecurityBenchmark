import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_audit_tools_mode() -> Dict[str, Any]:
    """
    Ensure audit tools mode is configured.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.2.4.8',
        'name': "Ensure audit tools mode is configured",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        audit_tools = ['/usr/sbin/auditctl', '/usr/sbin/audispd']  # Modify as needed
        correct_mode = 0o0755

        for tool in audit_tools:
            if os.path.exists(tool):
                tool_mode = oct(os.stat(tool).st_mode & 0o777)
                if tool_mode == oct(correct_mode):
                    result['status'] = True
                    result['details'] = f"{tool} has correct mode: {tool_mode}."
                    logger.info(result['details'])
                else:
                    result['details'] = f"{tool} does not have the correct mode: {tool_mode}."
                    logger.warning(result['details'])
            else:
                result['details'] = f"{tool} does not exist."
                logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking audit tools mode: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'audit_tools_mode': check_audit_tools_mode()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
