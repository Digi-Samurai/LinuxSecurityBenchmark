import os
import logging

logger = logging.getLogger(__name__)

def check_shadowed_passwords():
    """
    Ensure accounts in /etc/passwd use shadowed passwords.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '7.2.1',
        'name': "Ensure accounts in /etc/passwd use shadowed passwords",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        with open('/etc/passwd', 'r') as passwd_file:
            for line in passwd_file:
                fields = line.split(':')
                if fields[1] != 'x' and fields[1] != '*':  # Password field should be 'x' or '*'
                    result['details'] = f"Account {fields[0]} does not use a shadowed password"
                    logger.error(result['details'])
                    return result
        result['status'] = True
        result['details'] = "All accounts in /etc/passwd use shadowed passwords"
        logger.info(result['details'])
    except Exception as e:
        result['details'] = f"Error checking /etc/passwd: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'shadowed_passwords_check': check_shadowed_passwords()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
