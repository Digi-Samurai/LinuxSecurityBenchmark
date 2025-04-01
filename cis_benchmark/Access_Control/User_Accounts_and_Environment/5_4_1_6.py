import logging
import subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_last_password_change() -> Dict[str, Any]:
    """
    Ensure all users' last password change date is in the past.
    
    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.4.1.6',
        'name': "Ensure all users' last password change date is in the past",
        'status': False,
        'severity': 'medium',
        'details': ''
    }

    try:
        users_with_future_dates = []
        output = subprocess.run(
            ["chage", "-l", "root"], 
            capture_output=True, 
            text=True
        ).stdout

        all_users = subprocess.run(
            ["awk", "-F:", '{if ($3 >= 1000) print $1}', "/etc/passwd"], 
            capture_output=True, 
            text=True
        ).stdout.splitlines()

        for user in all_users:
            last_change_output = subprocess.run(
                ["chage", "-l", user], 
                capture_output=True, 
                text=True
            ).stdout
            
            for line in last_change_output.splitlines():
                if "Last password change" in line:
                    last_change_date = line.split(":")[1].strip()
                    
                    date_check = subprocess.run(
                        ["date", "-d", last_change_date, "+%s"], 
                        capture_output=True, 
                        text=True
                    )
                    
                    if date_check.returncode == 0:
                        last_change_timestamp = int(date_check.stdout.strip())
                        current_timestamp = int(subprocess.run(
                            ["date", "+%s"], capture_output=True, text=True
                        ).stdout.strip())

                        if last_change_timestamp > current_timestamp:
                            users_with_future_dates.append(user)

        if not users_with_future_dates:
            result['status'] = True
            result['details'] = "All users' last password change dates are in the past."
            logger.info(result['details'])
        else:
            result['details'] = f"Users with last password change in the future: {users_with_future_dates}"
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking last password change dates: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'last_password_change': check_last_password_change()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
