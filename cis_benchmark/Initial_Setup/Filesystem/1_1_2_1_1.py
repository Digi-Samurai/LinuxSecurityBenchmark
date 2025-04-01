import os
import subprocess
import logging

logger = logging.getLogger(__name__)

def check_tmp_separate_partition() -> dict:
    """
    Check if /tmp is a separate partition
    CIS Benchmark 1.1.2.1.1 - Ensure /tmp is a separate partition
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '1.1.2.1.1',
        'name': 'Ensure /tmp is a separate partition',
        'status': False,
        'severity': 'medium',
        'details': ''
    }
    
    try:
        # Use df to check if /tmp is a separate mount point
        df_cmd = "df /tmp | awk '$6 == \"/tmp\" {print}'"
        df_result = subprocess.run(
            df_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        # Check if the output is not empty (indicating a separate partition)
        if df_result.stdout.strip():
            result['status'] = True
            result['details'] = '/tmp is a separate partition'
            logger.info('/tmp is a separate partition')
        else:
            result['status'] = False
            result['details'] = '/tmp is not a separate partition'
            logger.warning('/tmp is not a separate partition')
    
    except Exception as e:
        result['status'] = False
        result['details'] = f'Error checking /tmp partition: {e}'
        logger.error(result['details'])
    
    return result

def run():
    """
    Run all checks for this benchmark section
    
    :return: Dictionary of check results
    """
    results = {
        'tmp_separate_partition': check_tmp_separate_partition()
    }
    
    return results

if __name__ == '__main__':
    # Direct execution for testing
    print(run())