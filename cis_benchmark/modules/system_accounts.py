```python
import subprocess
from termcolor import colored

def check_root_and_system_accounts():
    """Comprehensive checks for root and system accounts."""
    checks = {
        "UID 0 only for root": "awk -F: '$3 == 0 && $1 != \"root\"' /etc/passwd",
        "GID 0 only for root": "awk -F: '$4 == 0 && $1 != \"root\"' /etc/passwd",
        "Group root is the only GID 0": "awk -F: '$3 == 0 && $1 != \"root\"' /etc/group",
        "Root account access controlled": "ls -l /etc/securetty",
        "Root path integrity": "echo $PATH | grep -q '::' || echo $PATH | grep -q ':$'",
        "Root umask configured": "grep -E 'umask\s+0077' /etc/profile /etc/bash.bashrc",
        "System accounts do not have valid login shell": "awk -F: '($3<1000 && $1!=\"root\" && $7!=\"/usr/sbin/nologin\" && $7!=\"/bin/false\") {print}' /etc/passwd",
        "Accounts without valid login shell are locked": "awk -F: '($3<1000 && $1!=\"root\" && $2!~/^!|\\*/) {print}' /etc/shadow"
    }
    
    for check, command in checks.items():
        try:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.stdout.strip():
                print(colored(f"❌ {check} failed.", "red"))
            else:
                print(colored(f"✔️ {check} passed.", "green"))
        except Exception as e:
            print(colored(f"⚠️ Error checking {check}: {e}", "yellow"))
```