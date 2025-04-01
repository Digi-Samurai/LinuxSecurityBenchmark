import os
import logging

logger = logging.getLogger(__name__)

def check_duplicate_gids():
    """
    Ensure no duplicate GIDs exist.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '7.2.6',
        'name': "Ensure no duplicate GIDs exist",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        gids = {}
        with open('/etc/group', 'r') as group_file:
            for line in group_file:
                fields = line.split(':')
                gid = fields[2]
                if gid in gids:
                    result['details'] = f"Duplicate GID found: {gid}"
                    logger.error(result['details'])
                    return result
                gids[gid] = fields[0]
        result['status'] = True
        result['details'] = "No duplicate GIDs found"
        logger.info(result['details'])
    except Exception as e:
        result['details'] = f"Error checking for duplicate GIDs: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'duplicate_gids_check': check_duplicate_gids()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
