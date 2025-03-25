```python
import subprocess
from termcolor import colored

def check_package(package_name):
    """Check if a specific package is installed."""
    try:
        result = subprocess.run([
            "dpkg", "-l", package_name
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if package_name in result.stdout:
            print(colored(f"✔️ {package_name} is installed.", "green"))
        else:
            print(colored(f"❌ {package_name} is NOT installed.", "red"))
    except Exception as e:
        print(colored(f"⚠️ Error checking {package_name}: {e}", "yellow"))

def configure_pam_software_packages():
    """Check PAM-related software packages."""
    packages = ["pam", "libpam-modules", "libpam-pwquality"]
    for package in packages:
        check_package(package)
```