import os
import subprocess
import logging

logger = logging.getLogger(__name__)

def check_ptrace_scope() -> dict:
    """
    Ensure ptrace_scope is restricted.
    CIS Benchmark 1.5.2 - Ensure ptrace_scope is restricted.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.5.2',
        'name': 'Ensure ptrace_scope is restricted',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        with open('/proc/sys/kernel/yama/ptrace_scope', 'r') as f:
            value = f.read().strip()

        if value == '1':
            result['status'] = True
            result['details'] = f'ptrace_scope is restricted (value={value})'
            logger.info(result['details'])
        else:
            result['details'] = f'ptrace_scope is not restricted (value={value})'
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f'Error checking ptrace_scope: {e}'
        logger.error(result['details'])

    return result

def run():
    return {'ptrace_scope_restricted': check_ptrace_scope()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
