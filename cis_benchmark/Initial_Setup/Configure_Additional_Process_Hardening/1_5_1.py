import os
import subprocess
import logging

logger = logging.getLogger(__name__)

def check_aslr() -> dict:
    """
    Ensure Address Space Layout Randomization (ASLR) is enabled.
    CIS Benchmark 1.5.1 - Ensure ASLR is enabled.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.5.1',
        'name': 'Ensure ASLR is enabled',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        with open('/proc/sys/kernel/randomize_va_space', 'r') as f:
            value = f.read().strip()

        if value in ['1', '2']:
            result['status'] = True
            result['details'] = f'ASLR is enabled (value={value})'
            logger.info(result['details'])
        else:
            result['details'] = f'ASLR is disabled (value={value})'
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f'Error checking ASLR: {e}'
        logger.error(result['details'])

    return result

def run():
    return {'aslr_enabled': check_aslr()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
