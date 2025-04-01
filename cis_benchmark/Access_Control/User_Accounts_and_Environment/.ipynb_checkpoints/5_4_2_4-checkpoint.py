import logging
import os
import subprocess
from typing import Dict, Any

logger = logging.getLogger(__name__)

def check_root_account_access() -> Dict[str, Any]:
    """
    Ensure root account access is controlled.

    :return: Dictionary with check results
    """
    result = {
        'benchmark_id': '5.4.2.4',
        'name': "Ensure root account access is controlled",
        'status': False,
        'severity': 'high',
        'details': ''
    }

    try:
        # Check if root account is locked
        shadow_output = subprocess.run(
            ["awk", '-F:', '$1 == "root" {print $2}', "/etc/shadow"], 
            capture_output=True, 
            text=True
        ).stdout.strip()

        root_locked = shadow_output in ["*", "!", "!!"]

        # Check if root login is disabled via SSH
        sshd_config_path = "/etc/ssh/sshd_config"
        root_login_disabled = False

        if os.path.exists(sshd_config_path):
            with open(sshd_config_path, "r") as f:
                for line in f:
                    if line.strip().lower().startswith("permitrootlogin"):
                        if "no" in line.lower():
                            root_login_disabled = True
                        break

        # Check if direct root login is restricted in /etc/securetty
        securetty_path = "/etc/securetty"
        securetty_restricted = False

        if os.path.exists(securetty_path):
            with open(securetty_path, "r") as f:
                securetty_restricted = not any(line.strip() for line in f)

        # Determine overall compliance
        if root_locked and root_login_disabled and securetty_restricted:
            result['status'] = True
            result['details'] = "Root account access is properly controlled."
            logger.info(result['details'])
        else:
            missing_controls = []
            if not root_locked:
                missing_controls.append("Root account is not locked in /etc/shadow")
            if not root_login_disabled:
                missing_controls.append("Root login is not disabled in SSH configuration")
            if not securetty_restricted:
                missing_controls.append("Root access is allowed via /etc/securetty")

            result['details'] = "Root account access is not properly controlled: " + "; ".join(missing_controls)
            logger.warning(result['details'])

    except Exception as e:
        result['details'] = f"Error checking root account access: {e}"
        logger.error(result['details'])

    return result

def run():
    return {'root_account_access': check_root_account_access()}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(run())
