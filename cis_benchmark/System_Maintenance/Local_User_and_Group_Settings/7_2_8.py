import os
import logging

logger = logging.getLogger(__name__)

def check_duplicate_groupnames():
    """
    Ensure no duplicate group names exist.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '7.2.8',
        'name': "Ensure no duplicate group names exist",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        groupnames = {}
        with open('/etc/group', 'r') as group_file:
            for line in group_file:
                fields = line.split(':')
                groupname = fields[0]
                if groupname in groupnames:
                    result['details'] = f"Duplicate group name found: {groupname}"
                    logger.error(result['details'])
                    return result
                groupnames[groupname] = fields[2]
        result['status'] = True
        result['details'] = "No duplicate group names found"
        logger.info(result['details'])
    except Exception as e:
        result['details'] = f"Error checking for duplicate group names: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'duplicate_groupnames_check': check_duplicate_groupnames()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
