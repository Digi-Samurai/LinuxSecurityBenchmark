import subprocess
import logging

logger = logging.getLogger(__name__)

def check_var_log_audit_separate_partition() -> dict:
    """
    Check if /var/log/audit is a separate partition
    CIS Benchmark 1.1.2.7.1 - Ensure separate partition exists for /var/log/audit

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.1.2.7.1',
        'name': 'Ensure separate partition exists for /var/log/audit',
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        # Check if /var/log/audit is a separate mount point
        df_cmd = "df -h /var/log/audit"
        df_result = subprocess.run(df_cmd, shell=True, capture_output=True, text=True)

        if df_result.returncode == 0 and "/var/log/audit" in df_result.stdout:
            result['status'] = True
            result['details'] = '/var/log/audit is a separate partition'
            logger.info(result['details'])
        else:
            result['details'] = '/var/log/audit is not a separate partition'
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f'Error checking /var/log/audit partition: {e}'
        logger.error(result['details'])

    return result

def run():
    return {'var_log_audit_separate_partition': check_var_log_audit_separate_partition()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
