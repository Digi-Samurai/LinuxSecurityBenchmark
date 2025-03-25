```python
import subprocess
from termcolor import colored

def check_pam_module(module_name):
    """Check if a specific PAM module is enabled."""
    try:
        result = subprocess.run([
            "grep", module_name, "/etc/pam.d/common-auth"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if module_name in result.stdout:
            print(colored(f"✔️ {module_name} is enabled in PAM.", "green"))
        else:
            print(colored(f"❌ {module_name} is NOT enabled in PAM.", "red"))
    except Exception as e:
        print(colored(f"⚠️ Error checking {module_name}: {e}", "yellow"))

def configure_pam_auth_update_profiles():
    """Check PAM authentication modules."""
    pam_modules = ["pam_unix", "pam_faillock", "pam_pwquality", "pam_pwhistory"]
    for module in pam_modules:
        check_pam_module(module)

def check_faillock_settings():
    """Check faillock configuration settings."""
    settings = {
        "deny": "5",
        "unlock_time": "900",
        "even_deny_root": "true"
    }
    
    try:
        with open("/etc/security/faillock.conf", "r") as f:
            content = f.read()
            
            for key, expected_value in settings.items():
                if key in content and expected_value in content:
                    print(colored(f"✔️ {key} is set to {expected_value}.", "green"))
                else:
                    print(colored(f"❌ {key} is NOT correctly set.", "red"))
    except Exception as e:
        print(colored(f"⚠️ Error checking faillock settings: {e}", "yellow"))

def check_pwquality_settings():
    """Check password quality configuration settings."""
    settings = {
        "minlen": "14",
        "dcredit": "-1",
        "ucredit": "-1",
        "lcredit": "-1",
        "ocredit": "-1",
        "maxrepeat": "3",
        "maxsequence": "4",
        "dictcheck": "1"
    }
    
    try:
        with open("/etc/security/pwquality.conf", "r") as f:
            content = f.read()
            
            for key, expected_value in settings.items():
                if key in content and expected_value in content:
                    print(colored(f"✔️ {key} is set to {expected_value}.", "green"))
                else:
                    print(colored(f"❌ {key} is NOT correctly set.", "red"))
    except Exception as e:
        print(colored(f"⚠️ Error checking pwquality settings: {e}", "yellow"))

def check_shadow_password_settings():
    """Check shadow password configuration settings."""
    settings = {
        "PASS_MAX_DAYS": "90",
        "PASS_MIN_DAYS": "1",
        "PASS_WARN_AGE": "7",
        "ENCRYPT_METHOD": "SHA512",
        "INACTIVE": "30"
    }
    
    try:
        with open("/etc/login.defs", "r") as f:
            content = f.read()
            
            for key, expected_value in settings.items():
                if key in content and expected_value in content:
                    print(colored(f"✔️ {key} is set to {expected_value}.", "green"))
                else:
                    print(colored(f"❌ {key} is NOT correctly set.", "red"))
    except Exception as e:
        print(colored(f"⚠️ Error checking shadow password settings: {e}", "yellow"))
```