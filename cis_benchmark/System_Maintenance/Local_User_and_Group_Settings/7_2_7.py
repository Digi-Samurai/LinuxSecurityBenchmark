import os
import logging

logger = logging.getLogger(__name__)

def check_duplicate_usernames():
    """
    Ensure no duplicate user names exist.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '7.2.7',
        'name': "Ensure no duplicate user names exist",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        usernames = {}
        with open('/etc/passwd', 'r') as passwd_file:
            for line in passwd_file:
                fields = line.split(':')
                username = fields[0]
                if username in usernames:
                    result['details'] = f"Duplicate username found: {username}"
                    logger.error(result['details'])
                    return result
                usernames[username] = fields[2]
        result['status'] = True
        result['details'] = "No duplicate usernames found"
        logger.info(result['details'])
    except Exception as e:
        result['details'] = f"Error checking for duplicate usernames: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'duplicate_usernames_check': check_duplicate_usernames()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
