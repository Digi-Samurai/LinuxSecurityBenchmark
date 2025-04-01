import os
import logging

logger = logging.getLogger(__name__)

def check_groups_in_passwd_and_group():
    """
    Ensure all groups in /etc/passwd exist in /etc/group.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '7.2.3',
        'name': "Ensure all groups in /etc/passwd exist in /etc/group",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Get list of groups in /etc/passwd
        with open('/etc/passwd', 'r') as passwd_file:
            passwd_groups = {line.split(':')[3] for line in passwd_file if line.strip()}

        # Get list of groups in /etc/group
        with open('/etc/group', 'r') as group_file:
            group_names = {line.split(':')[0] for line in group_file if line.strip()}

        # Check for missing groups
        missing_groups = passwd_groups - group_names
        if missing_groups:
            result['details'] = f"Groups in /etc/passwd but not in /etc/group: {missing_groups}"
            logger.error(result['details'])
        else:
            result['status'] = True
            result['details'] = "All groups in /etc/passwd exist in /etc/group"
            logger.info(result['details'])
    except Exception as e:
        result['details'] = f"Error checking /etc/passwd or /etc/group: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'groups_in_passwd_and_group_check': check_groups_in_passwd_and_group()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
