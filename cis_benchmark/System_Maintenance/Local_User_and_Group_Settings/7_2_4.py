import os
import logging

logger = logging.getLogger(__name__)

def check_shadow_group_empty():
    """
    Ensure shadow group is empty.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '7.2.4',
        'name': "Ensure shadow group is empty",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        with open('/etc/group', 'r') as group_file:
            for line in group_file:
                if line.startswith('shadow:'):
                    fields = line.split(':')
                    if len(fields) > 3 and fields[3]:  # Check if group has members
                        result['details'] = f"Shadow group is not empty: {fields[3]}"
                        logger.error(result['details'])
                        return result
        result['status'] = True
        result['details'] = "Shadow group is empty"
        logger.info(result['details'])
    except Exception as e:
        result['details'] = f"Error checking /etc/group: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'shadow_group_empty_check': check_shadow_group_empty()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
