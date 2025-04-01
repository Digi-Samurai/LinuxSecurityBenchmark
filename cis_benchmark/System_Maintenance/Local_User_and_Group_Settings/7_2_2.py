import os
import logging

logger = logging.getLogger(__name__)

def check_shadow_password_fields():
    """
    Ensure /etc/shadow password fields are not empty.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '7.2.2',
        'name': "Ensure /etc/shadow password fields are not empty",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        with open('/etc/shadow', 'r') as shadow_file:
            for line in shadow_file:
                fields = line.split(':')
                if len(fields) > 1 and fields[1] == '':
                    result['details'] = f"Account {fields[0]} has an empty password field in /etc/shadow"
                    logger.error(result['details'])
                    return result
        result['status'] = True
        result['details'] = "No empty password fields found in /etc/shadow"
        logger.info(result['details'])
    except Exception as e:
        result['details'] = f"Error checking /etc/shadow: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'shadow_password_fields_check': check_shadow_password_fields()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
