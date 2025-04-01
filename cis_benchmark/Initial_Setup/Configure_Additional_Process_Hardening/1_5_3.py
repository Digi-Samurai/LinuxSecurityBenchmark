import os
import subprocess
import logging

logger = logging.getLogger(__name__)

def check_core_dumps() -> dict:
    """
    Ensure core dumps are restricted.
    CIS Benchmark 1.5.3 - Ensure core dumps are restricted.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.5.3',
        'name': 'Ensure core dumps are restricted',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        with open('/etc/security/limits.conf', 'r') as f:
            lines = f.readlines()

        core_dump_restricted = any(
            "* hard core 0" in line for line in lines
        )

        if core_dump_restricted:
            result['status'] = True
            result['details'] = 'Core dumps are restricted in limits.conf'
            logger.info(result['details'])
        else:
            result['details'] = 'Core dumps are NOT restricted in limits.conf'
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f'Error checking core dumps: {e}'
        logger.error(result['details'])

    return result

def run():
    return {'core_dumps_restricted': check_core_dumps()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
