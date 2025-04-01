import os
import logging

logger = logging.getLogger(__name__)

def check_duplicate_uids():
    """
    Ensure no duplicate UIDs exist.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '7.2.5',
        'name': "Ensure no duplicate UIDs exist",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        uids = {}
        with open('/etc/passwd', 'r') as passwd_file:
            for line in passwd_file:
                fields = line.split(':')
                uid = fields[2]
                if uid in uids:
                    result['details'] = f"Duplicate UID found: {uid}"
                    logger.error(result['details'])
                    return result
                uids[uid] = fields[0]
        result['status'] = True
        result['details'] = "No duplicate UIDs found"
        logger.info(result['details'])
    except Exception as e:
        result['details'] = f"Error checking for duplicate UIDs: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'duplicate_uids_check': check_duplicate_uids()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
