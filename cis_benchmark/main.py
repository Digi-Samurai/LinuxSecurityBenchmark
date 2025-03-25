```python
from termcolor import colored
from cis_benchmark.utils import run_check, time_sync_run_check

def check_time_sync(time_services=None, chrony_services=None):
    """Check if a single time synchronization daemon is in use and properly configured."""
    active_services = []

    # Default services if not provided
    if time_services is None:
        time_services = {
            "check": "systemctl is-active systemd-timesyncd",
            "config": "timedatectl show-timesync --property=ServerName",
            "user_check": None
        }
    
    if chrony_services is None:
        chrony_services = {
            "check": "systemctl is-active chronyd",
            "config": "chronyc sources",
            "user_check": "ps aux | grep _chrony"
        }

    services = {
        "systemd-timesyncd": time_services,
        "chrony": chrony_services
    }

    for service_name, cmds in services.items():
        is_active, _ = time_sync_run_check(cmds["check"])
        if is_active:
            active_services.append(service_name)
            print(colored(f"✅ {service_name} is active.", "green"))

            if cmds.get("config"):
                configured, output = time_sync_run_check(cmds["config"])
                if configured and output:
                    print(colored(f"✅ {service_name} is configured with an authorized timeserver.", "green"))
                else:
                    print(colored(f"❌ {service_name} is not properly configured!", "red"))

            if cmds.get("user_check"):
                user_running, output = time_sync_run_check(cmds["user_check"])
                if service_name == "chrony" and user_running and "_chrony" in output:
                    print(colored("✅ chronyd is running as user _chrony.", "green"))
                else:
                    print(colored("❌ chronyd is not running as user _chrony!", "red"))

    if len(active_services) > 1:
        print(colored("❌ More than one time synchronization daemon is active!", "red"))
    elif len(active_services) == 0:
        print(colored("❌ No time synchronization daemon is active!", "red"))
    else:
        print(colored("✅ A single time synchronization daemon is correctly in use.", "green"))

def check_cron_enabled():
    """Check if cron daemon is enabled and active."""
    result = run_check("systemctl is-active cron")
    if result == "active":
        print(colored("✅ cron daemon is enabled and active.", "green"))
    else:
        print(colored("❌ cron daemon is NOT enabled or active!", "red"))

def check_cron_config():
    """Checks the permissions of common cron configuration files."""
    print(colored("\nChecking Cron Configuration Files Permissions:", "yellow", attrs=["bold"]))
    check_cron_permissions("/etc/crontab", 0o644)
    check_cron_permissions("/etc/cron.d", 0o755)
    check_cron_permissions("/etc/cron.daily", 0o755)
    check_cron_permissions("/etc/cron.hourly", 0o755)
    check_cron_permissions("/etc/cron.monthly", 0o755)
    check_cron_permissions("/etc/cron.weekly", 0o755)

def check_cron_permissions(filepath, expected_mode):
    """Check permissions on cron-related files."""
    import os
    import stat

    if os.path.exists(filepath):
        mode = os.stat(filepath).st_mode
        current_perms = oct(mode & 0o777)
        expected_perms_str = oct(expected_mode)[-3:]
        if current_perms == expected_perms_str:
            print(colored(f"✅ Permissions on {filepath} are configured correctly ({current_perms}).", "green"))
        else:
            print(colored(f"❌ Incorrect permissions on {filepath}! Expected {expected_perms_str}, found {current_perms}.", "red"))
    else:
        print(colored(f"⚠️ {filepath} not found.", "yellow"))

def check_crontab_restricted():
    """Check if crontab is restricted to authorized users."""
    result = run_check("ls -l /etc/cron.allow")
    if result:
        print(colored("✅ crontab access is restricted using /etc/cron.allow.", "green"))
    else:
        print(colored("❌ crontab access is not restricted using /etc/cron.allow!", "red"))

def check_at_restricted():
    """Check if at is restricted to authorized users."""
    result = run_check("ls -l /etc/at.allow")
    if result:
        print(colored("✅ 'at' access is restricted using /etc/at.allow.", "green"))
    else:
        print(colored("❌ 'at' access is not restricted using /etc/at.allow!", "red"))
```