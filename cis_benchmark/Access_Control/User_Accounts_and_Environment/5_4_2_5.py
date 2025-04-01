import logging
import os
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_root_path_integrity() -> Dict[str, Any]:
    """
    Ensure root path integrity.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.4.2.5',
        'name': 'Ensure root path integrity',
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        paths = os.environ.get('PATH', '').split(':')
        insecure_paths = [p for p in paths if p.startswith('.') or not os.path.exists(p)]

        if insecure_paths:
            result['details'] = f"Insecure paths found: {', '.join(insecure_paths)}"
            logger.warning(result['details'])
        else:
            result['status'] = True
            result['details'] = "Root PATH integrity is ensured."
            logger.info(result['details'])

    except Exception as e:
        result['details'] = f"Error checking root path integrity: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'root_path_integrity': check_root_path_integrity()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
