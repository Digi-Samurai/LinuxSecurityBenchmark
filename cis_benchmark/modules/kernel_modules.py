```python
from termcolor import colored
from cis_benchmark.utils import run_check

def check_kernel_modules():
    """Checks for the availability of specific kernel modules."""
    print(colored("\n3.2 Configure Network Kernel Modules", "yellow", attrs=["bold"]))
    modules_to_check = {
        "dccp": "dccp",
        "tipc": "tipc",
        "rds": "rds",
        "sctp": "sctp"
    }
    for module, name in modules_to_check.items():
        command = f"lsmod | grep -i {name}"
        result = run_check(command)
        if result:
            print(colored(f"❌ {module} kernel module is available!", "red"))
        else:
            print(colored(f"✅ {module} kernel module is NOT available.", "green"))
```