import subprocess
import logging

logger = logging.getLogger(__name__)

def check_home_separate_partition() -> dict:
    """
    Check if /home is a separate partition
    CIS Benchmark 1.1.2.3.1 - Ensure separate partition exists for /home

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.1.2.3.1',
        'name': 'Ensure separate partition exists for /home',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        # Use df to check if /home is a separate mount point
        df_cmd = "df -h /home"
        df_result = subprocess.run(df_cmd, shell=True, capture_output=True, text=True)

        if df_result.returncode == 0 and "/home" in df_result.stdout:
            result['status'] = True
            result['details'] = '/home is a separate partition'
            logger.info(result['details'])
        else:
            result['details'] = '/home is not a separate partition'
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f'Error checking /home partition: {e}'
        logger.error(result['details'])

    return result

def run():
    return {'home_separate_partition': check_home_separate_partition()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
