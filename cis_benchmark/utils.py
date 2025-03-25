```python
import subprocess
import os
from termcolor import colored

def run_check(command, shell=True):
    """
    Run a shell command and return its output.
    
    Args:
        command (str or list): Command to run
        shell (bool): Whether to use shell
    
    Returns:
        str or None: Command output or None if error
    """
    try:
        result = subprocess.run(
            command, 
            shell=shell, 
            capture_output=True, 
            text=True, 
            check=False
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception as e:
        print(colored(f"Error executing command: {e}", "red"))
        return None

def print_check_result(check_name, status, success_msg=None, failure_msg=None):
    """
    Print standardized check results.
    
    Args:
        check_name (str): Name of the security check
        status (bool): Whether the check passed
        success_msg (str, optional): Custom success message
        failure_msg (str, optional): Custom failure message
    """
    if status:
        print(colored(f"✅ {check_name}: {success_msg or 'Passed'}", "green"))
    else:
        print(colored(f"❌ {check_name}: {failure_msg or 'Failed'}", "red"))

def read_file_content(filepath):
    """
    Read content of a file safely.
    
    Args:
        filepath (str): Path to the file
    
    Returns:
        str or None: File content or None if error
    """
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        print(colored(f"Error reading {filepath}: {e}", "yellow"))
        return None
```