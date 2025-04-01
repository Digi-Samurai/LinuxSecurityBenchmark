import logging
import subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_logfile_access() -> Dict[str, Any]:
    """
    Ensure access to all log files has been configured properly.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '6.1.4.1',
        'name': "Ensure access to all log files has been configured",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check the permissions for log files in /var/log
        log_files = subprocess.run(
            ['find', '/var/log', '-type f', '-exec', 'ls', '-l', '{}', ';'],
            capture_output=True,
            text=True
        )
        
        # Analyze output and check permissions
        log_files_output = log_files.stdout
        lines = log_files_output.splitlines()
        
        # Check for proper permissions (only root or specific users should have access)
        for line in lines:
            if not line:
                continue
            parts = line.split()
            permissions = parts[0]
            owner = parts[2]
            group = parts[3]

            # Check if the log file is accessible by unauthorized users (should not be world-readable or writable)
            if 'r' not in permissions[7:10] or 'w' not in permissions[7:10]:
                result['status'] = True
                result['details'] = "Access to log files is properly configured with restricted permissions."
                logger.info(result['details'])
            else:
                result['details'] = f"Log file {parts[-1]} has insecure permissions. Please review."
                logger.warning(result['details'])
                return result  # Return failure if any file is insecure

    except Exception as e:
        result['details'] = f"Error checking log file access permissions: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'logfile_access': check_logfile_access()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
