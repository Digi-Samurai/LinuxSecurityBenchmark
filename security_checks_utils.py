# utils.py
import subprocess
from termcolor import colored
import os
import stat

def run_check(command):
    """Run a shell command and return its output or False on error."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return False

def check_module(module):
    """Check if a kernel module is loaded."""
    result = run_check("lsmod")
    if result and module in result:
        print(colored(f"❌ {module} module is loaded!", "red"))
    else:
        print(colored(f"✅ {module} module is NOT loaded.", "green"))

def check_partition(partition):
    """Check if a partition exists."""
    result = run_check("mount")
    if result and partition in result:
        print(colored(f"✅ {partition} is a separate partition.", "green"))
    else:
        print(colored(f"❌ {partition} is NOT a separate partition!", "red"))

def check_mount_options(partition, options):
    """Check if specific mount options are set for a partition."""
    result = run_check("mount")
    if result:
        found_partition = False
        for line in result.split("\n"):
            if partition in line:
                found_partition = True
                for option in options:
                    if option in line:
                        print(colored(f"✅ {option} is set on {partition}.", "green"))
                    else:
                        print(colored(f"❌ {option} is NOT set on {partition}!", "red"))
                return
        if not found_partition:
            print(colored(f"❌ {partition} is not found in mount points!", "red"))
    else:
        print(colored("Error running 'mount' command.", "red"))

def InitialSetup_config(name, command):
    """Run system configuration checks."""
    result = run_check(command)
    if result:
        print(colored(f"✅ {name} is configured.", "green"))
    else:
        print(colored(f"❌ {name} is NOT configured!", "red"))

def Server_Services_Check(service, command):
    """Check if a server service is active or installed."""
    result = run_check(command)
    if command.startswith("systemctl is-active"):
        if result == "active":
            print(colored(f"❌ {service} is running!", "red"))
        else:
            print(colored(f"✅ {service} is not running.", "green"))
    elif command.startswith("dpkg -l | grep -i"):
        if result:
            print(colored(f"❌ {service} is installed!", "red"))
        else:
            print(colored(f"✅ {service} is not installed.", "green"))
    else:
        print(colored(f"⚠️ Unknown command type for service check: {command}", "yellow"))

def Client_Services_Check(service, command):
    """Check if a client service is installed."""
    result = run_check(command)
    if result:
        print(colored(f"❌ {service} is installed!", "red"))
    else:
        print(colored(f"✅ {service} is not installed.", "green"))

def time_sync_run_check(command):
    """Run a shell command and return True if successful, False otherwise."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        return False, str(e)

def check_time_sync(time_services, chrony_services):
    """Check if a single time synchronization daemon is in use and properly configured."""
    active_services = []

    services = {
        "systemd-timesyncd": time_services,
        "chrony": chrony_services
    }

    for service_name, cmds in services.items():
        is_active, _ = time_sync_run_check(cmds["check"])
        if is_active:
            active_services.append(service_name)
            print(colored(f"✅ {service_name} is active.", "green"))

            if cmds["config"]:
                configured, output = time_sync_run_check(cmds["config"])
                if configured and output:
                    print(colored(f"✅ {service_name} is configured with an authorized timeserver.", "green"))
                else:
                    print(colored(f"❌ {service_name} is not properly configured!", "red"))

            if cmds["user_check"]:
                user_running, output = time_sync_run_check(cmds["user_check"])
                if user_running and "_chrony" in output:
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

def check_cron_permissions(filepath, expected_mode):
    """Check permissions on cron-related files."""
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

def check_cron_config():
    """Checks the permissions of common cron configuration files."""
    print(colored("\nChecking Cron Configuration Files Permissions:", "yellow", attrs=["bold"]))
    check_cron_permissions("/etc/crontab", 0o644)
    check_cron_permissions("/etc/cron.d", 0o755)
    check_cron_permissions("/etc/cron.daily", 0o755)
    check_cron_permissions("/etc/cron.hourly", 0o755)
    check_cron_permissions("/etc/cron.monthly", 0o755)
    check_cron_permissions("/etc/cron.weekly", 0o755)

def check_ipv6_status():
    """Identifies the IPv6 status (Manual check - no automated command)."""
    print(colored("\n3.1.1 Ensure IPv6 status is identified (Manual)", "yellow", attrs=["bold"]))
    print(colored("Please manually verify the IPv6 status of the system.", "cyan"))
    print(colored("This check cannot be automated.", "cyan"))

def check_wireless_disabled():
    """Ensure wireless interfaces are disabled."""
    print(colored("\n3.1.2 Ensure wireless interfaces are disabled (Automated)", "yellow", attrs=["bold"]))
    result = run_check("ip link show | grep -E 'wlan[0-9]+'")
    if result:
        print(colored("❌ Wireless interfaces are present and may be enabled.", "red"))
        print(colored("Consider disabling them using 'sudo ip link set <interface_name> down'.", "yellow"))
    else:
        print(colored("✅ No active wireless interfaces found.", "green"))

def check_bluetooth_inactive():
    """Ensure bluetooth services are not in use."""
    print(colored("\n3.1.3 Ensure bluetooth services are not in use (Automated)", "yellow", attrs=["bold"]))
    result = run_check("systemctl is-active bluetooth")
    if result == "active":
        print(colored("❌ Bluetooth service is running!", "red"))
    else:
        print(colored("✅ Bluetooth service is not running.", "green"))

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

def check_network_parameters():
    """Checks various network kernel parameters."""
    print(colored("\n3.3 Configure Network Kernel Parameters", "yellow", attrs=["bold"]))
    params_to_check = {
        "net.ipv4.ip_forward": "0",
        "net.ipv4.conf.all.send_redirects": "0",
        "net.ipv4.icmp_ignore_bogus_error_responses": "1",
        "net.ipv4.icmp_echo_ignore_broadcasts": "1",
        "net.ipv4.conf.all.accept_redirects": "0",
        "net.ipv4.conf.all.secure_redirects": "0",
        "net.ipv4.conf.all.rp_filter": "1",
        "net.ipv4.conf.all.accept_source_route": "0",
        "net.ipv4.conf.all.log_martian": "1",
        "net.ipv4.tcp_syncookies": "1",
        "net.ipv6.conf.all.accept_ra": "0"
    }
    for param, expected_value in params_to_check.items():
        command = f"sysctl -n {param}"
        result = run_check(command)
        if result == expected_value:
            print(colored(f"✅ {param} is set to {expected_value}.", "green"))
        else:
            print(colored(f"❌ {param} is NOT set to {expected_value}! (Current: {result if result else 'Error'})", "red"))

def check_single_firewall():
    """Ensure a single firewall configuration utility is in use."""
    print(colored("\n4.1 Configure a single firewall utility", "yellow", attrs=["bold"]))
    ufw_installed = run_check("dpkg -s ufw | grep -q 'install ok'")
    nftables_installed = run_check("dpkg -s nftables | grep -q 'install ok'")
    iptables_installed = run_check("dpkg -s iptables | grep -q 'install ok'")

    active_firewalls = []
    if ufw_installed:
        active_firewalls.append("ufw")
    if nftables_installed:
        active_firewalls.append("nftables")
    if iptables_installed:
        active_firewalls.append("iptables")

    if len(active_firewalls) == 1:
        print(colored(f"✅ Only one firewall utility ({active_firewalls[0]}) is in use.", "green"))
    elif len(active_firewalls) > 1:
        print(colored(f"❌ Multiple firewall utilities are installed: {', '.join(active_firewalls)}", "red"))
        print(colored("Ensure only one firewall is actively managing the system.", "yellow"))
    else:
        print(colored("⚠️ No firewall utility (ufw, nftables, iptables) appears to be installed.", "yellow"))

def check_ufw():
    """Checks for UncomplicatedFirewall configuration."""
    print(colored("\n4.2 Configure UncomplicatedFirewall", "yellow", attrs=["bold"]))
    ufw_installed = run_check("dpkg -s ufw | grep -q 'install ok'")
    if ufw_installed:
        print(colored("✅ ufw is installed.", "green"))
        # 4.2.2 Ensure iptables-persistent is not installed with ufw
        iptables_persistent_installed = run_check("dpkg -s iptables-persistent | grep -q 'install ok'")
        if iptables_persistent_installed:
            print(colored("❌ iptables-persistent is installed alongside ufw!", "red"))
            print(colored("Consider removing iptables-persistent if using ufw.", "yellow"))
        else:
            print(colored("✅ iptables-persistent is not installed with ufw.", "green"))

        # 4.2.3 Ensure ufw service is enabled
        ufw_enabled_result = run_check("systemctl is-enabled ufw")
        if ufw_enabled_result == "enabled":
            print(colored("✅ ufw service is enabled.", "green"))
        else:
            print(colored("❌ ufw service is NOT enabled!", "red"))

        # 4.2.4 Ensure ufw loopback traffic is configured
        loopback_rule_check = run_check("ufw status numbered | grep 'ALLOW IN ON lo'")
        if loopback_rule_check:
            print(colored("✅ ufw loopback traffic is configured.", "green"))
        else:
            print(colored("❌ ufw loopback traffic is NOT configured!", "red"))
            print(colored("Consider adding a rule: 'sudo ufw allow in on lo'.", "yellow"))

        # 4.2.5 Ensure ufw outbound connections are configured (Manual)
        print(colored("⚠️ 4.2.5 Ensure ufw outbound connections are configured (Manual)", "yellow"))
        print(colored("Please manually review your ufw rules to ensure outbound connections are configured as needed.", "cyan"))

        # 4.2.6 Ensure ufw firewall rules exist for all open ports
        print(colored("⚠️ 4.2.6 Ensure ufw firewall rules exist for all open ports (Automated)", "yellow"))
        print(colored("Automated check for specific open port rules is complex. Manually review ufw rules.", "cyan"))

        # 4.2.7 Ensure ufw default deny firewall policy
        default_deny_result = run_check("ufw status verbose | grep 'Default: deny'")
        if default_deny_result:
            print(colored("✅ ufw default deny firewall policy is configured.", "green"))
        else:
            print(colored("❌ ufw default deny firewall policy is NOT configured!", "red"))
            print(colored("Set default policy with 'sudo ufw default deny incoming' and 'sudo ufw default deny outgoing'.", "yellow"))
    else:
        print(colored("❌ ufw is NOT installed.", "red"))

def check_nftables():
    """Checks for nftables configuration."""
    print(colored("\n4.3 Configure nftables", "yellow", attrs=["bold"]))
    nftables_installed = run_check("dpkg -s nftables | grep -q 'install ok'")
    if nftables_installed:
        print(colored("✅ nftables is installed.", "green"))

        # 4.3.2 Ensure ufw is uninstalled or disabled with nftables
        ufw_installed = run_check("dpkg -s ufw | grep -q 'install ok'")
        ufw_active = run_check("systemctl is-active ufw")
        if ufw_installed and ufw_active == "active":
            print(colored("❌ ufw is installed and active alongside nftables!", "red"))
            print(colored("Consider uninstalling or disabling ufw.", "yellow"))
        elif ufw_installed:
            print(colored("⚠️ ufw is installed but not active alongside nftables.", "yellow"))
        else:
            print(colored("✅ ufw is not installed or active.", "green"))

        # 4.3.3 Ensure iptables are flushed with nftables (Manual)
        print(colored("⚠️ 4.3.3 Ensure iptables are flushed with nftables (Manual)", "yellow"))
        print(colored("Please manually verify that iptables rules have been flushed if using nftables.", "cyan"))

        # 4.3.4 Ensure a nftables table exists
        table_exists = run_check("nft list tables | grep inet")
        if table_exists:
            print(colored("✅ A nftables table exists.", "green"))
        else:
            print(colored("❌ No nftables table found!", "red"))
            print(colored("Consider creating a table: 'sudo nft create table inet filter'.", "yellow"))

        # 4.3.5 Ensure nftables base chains exist
        base_chains_check = run_check("nft list chain inet filter input | grep -E 'type filter hook input priority 0;' && nft list chain inet filter forward | grep -E 'type filter hook forward priority 0;' && nft list chain inet filter output | grep -E 'type filter hook output priority 0;'")
        if base_chains_check:
            print(colored("✅ nftables base chains (input, forward, output) exist.", "green"))
        else:
            print(colored("❌ nftables base chains (input, forward, output) do not exist!", "red"))
            print(colored("Consider creating them: 'sudo nft add table inet filter' followed by 'sudo nft add chain inet filter input { type filter hook input priority 0 \; }', 'sudo nft add chain inet filter forward { type filter hook forward priority 0 \; }', 'sudo nft add chain inet filter output { type filter hook output priority 0 \; }'.", "yellow"))

        # 4.3.6 Ensure nftables loopback traffic is configured
        loopback_rule_check = run_check("nft list rules inet filter input | grep 'iif lo accept'")
        if loopback_rule_check:
            print(colored("✅ nftables loopback traffic is configured.", "green"))
        else:
            print(colored("❌ nftables loopback traffic is NOT configured!", "red"))
            print(colored("Consider adding a rule: 'sudo nft add rule inet filter input iif lo accept'.", "yellow"))

        # 4.3.7 Ensure nftables outbound and established connections are configured (Manual)
        print(colored("⚠️ 4.3.7 Ensure nftables outbound and established connections are configured (Manual)", "yellow"))
        print(colored("Please manually review your nftables rules to ensure outbound and established connections are configured as needed.", "cyan"))

        # 4.3.8 Ensure nftables default deny firewall policy
        default_deny_input = run_check("nft list rules inet filter input | grep 'policy drop'")
        default_deny_forward = run_check("nft list rules inet filter forward | grep 'policy drop'")
        default_deny_output = run_check("nft list rules inet filter output | grep 'policy accept'") # Generally accept for output
        if default_deny_input and default_deny_forward and default_deny_output:
            print(colored("✅ nftables default deny firewall policy (input and forward) is configured.", "green"))
        else:
            print(colored("❌ nftables default deny firewall policy (input or forward) is NOT configured!", "red"))
            print(colored("Set default policies with 'sudo nft -f - <<EOF\\ntable inet filter\\nflush table inet filter\\nchain input { type filter hook input priority 0; policy drop; }\\nchain forward { type filter hook forward priority 0; policy drop; }\\nchain output { type filter hook output priority 0; policy accept; }\\nEOF'", "yellow"))

        # 4.3.9 Ensure nftables service is enabled
        nftables_enabled_result = run_check("systemctl is-enabled nftables")
        if nftables_enabled_result == "enabled":
            print(colored("✅ nftables service is enabled.", "green"))
        else:
            print(colored("❌ nftables service is NOT enabled!", "red"))

        # 4.3.10 Ensure nftables rules are permanent
        print(colored("⚠️ 4.3.10 Ensure nftables rules are permanent (Automated)", "yellow"))
        print(colored("Rules are generally made permanent by saving them (e.g., using 'sudo nft list rules inet filter > /etc/nftables.conf' and enabling the service). Verify configuration.", "cyan"))
    else:
        print(colored("❌ nftables is NOT installed.", "red"))

def check_iptables():
    """Checks for iptables configuration."""
    print(colored("\n4.4 Configure iptables", "yellow", attrs=["bold"]))
    iptables_installed = run_check("dpkg -s iptables | grep -q 'install ok'")
    if iptables_installed:
        print(colored("✅ iptables packages are installed.", "green"))

        # 4.4.1.2 Ensure nftables is not in use with iptables
        nftables_installed = run_check("dpkg -s nftables | grep -q 'install ok'")
        if nftables_installed:
            print(colored("❌ nftables is installed alongside iptables!", "red"))
            print(colored("Consider uninstalling nftables if using iptables.", "yellow"))
        else:
            print(colored("✅ nftables is not in use with iptables.", "green"))

        # 4.4.1.3 Ensure ufw is not in use with iptables
        ufw_installed = run_check("dpkg -s ufw | grep -q 'install ok'")
        if ufw_installed:
            print(colored("❌ ufw is installed alongside iptables!", "red"))
            print(colored("Consider uninstalling ufw if using iptables directly.", "yellow"))
        else:
            print(colored("✅ ufw is not in use with iptables.", "green"))

        # 4.4.2 Configure IPv4 iptables
        print(colored("\n4.4.2 Configure IPv4 iptables", "yellow", attrs=["bold"]))

        # 4.4.2.1 Ensure iptables default deny firewall policy
        default_deny_input = run_check("iptables -P INPUT DROP")
        default_deny_forward = run_check("iptables -P FORWARD DROP")
        default_accept_output = run_check("iptables -P OUTPUT ACCEPT")
        if default_deny_input and default_deny_forward and default_accept_output:
            print(colored("✅ iptables default deny firewall policy (input and forward) is configured.", "green"))
        else:
            print(colored("❌ iptables default deny firewall policy (input or forward) is NOT configured!", "red"))
            print(colored("Set default policies with 'sudo iptables -P INPUT DROP', 'sudo iptables -P FORWARD DROP', and 'sudo iptables -P OUTPUT ACCEPT'.", "yellow"))

        # 4.4.2.2 Ensure iptables loopback traffic is configured
        loopback_rule_check = run_check("iptables -L INPUT -n | grep 'lo'")
        if loopback_rule_check:
            print(colored("✅ iptables loopback traffic is configured.", "green"))
        else:
            print(colored("❌ iptables loopback traffic is NOT configured!", "red"))
            print(colored("Consider adding a rule: 'sudo iptables -A INPUT -i lo -j ACCEPT'.", "yellow"))

        # 4.4.2.3 Ensure iptables outbound and established connections are configured (Manual)
        print(colored("⚠️ 4.4.2.3 Ensure iptables outbound and established connections are configured (Manual)", "yellow"))
        print(colored("Please manually review your iptables rules to ensure outbound and established connections are configured as needed.", "cyan"))

        # 4.4.2.4 Ensure iptables firewall rules exist for all open ports
        print(colored("⚠️ 4.4.2.4 Ensure iptables firewall rules exist for all open ports (Automated)", "yellow"))
        print(colored("Automated check for specific open port rules is complex. Manually review iptables rules.", "cyan"))

        # 4.4.3 Configure IPv6 ip6tables
        print(colored("\n4.4.3 Configure IPv6 ip6tables", "yellow", attrs=["bold"]))

        # 4.4.3.1 Ensure ip6tables default deny firewall policy
        default_deny_input6 = run_check("ip6tables -P INPUT DROP")
        default_deny_forward6 = run_check("ip6tables -P FORWARD DROP")
        default_accept_output6 = run_check("ip6tables -P OUTPUT ACCEPT")
        if default_deny_input6 and default_deny_forward6 and default_accept_output6:
            print(colored("✅ ip6tables default deny firewall policy (input and forward) is configured.", "green"))
        else:
            print(colored("❌ ip6tables default deny firewall policy (input or forward) is NOT configured!", "red"))
            print(colored("Set default policies with 'sudo ip6tables -P INPUT DROP', 'sudo ip6tables -P FORWARD DROP', and 'sudo ip6tables -P OUTPUT ACCEPT'.", "yellow"))

        # 4.4.3.2 Ensure ip6tables loopback traffic is configured
        loopback_rule_check6 = run_check("ip6tables -L INPUT -n | grep 'lo'")
        if loopback_rule_check6:
            print(colored("✅ ip6tables loopback traffic is configured.", "green"))
        else:
            print(colored("❌ ip6tables loopback traffic is NOT configured!", "red"))
            print(colored("Consider adding a rule: 'sudo ip6tables -A INPUT -i lo -j ACCEPT'.", "yellow"))

        # 4.4.3.3 Ensure ip6tables outbound and established connections are configured (Manual)
        print(colored("⚠️ 4.4.3.3 Ensure ip6tables outbound and established connections are configured (Manual)", "yellow"))
        print(colored("Please manually review your ip6tables rules to ensure outbound and established connections are configured as needed.", "cyan"))

        # 4.4.3.4 Ensure ip6tables firewall rules exist for all open ports
        print(colored("⚠️ 4.4.3.4 Ensure ip6tables firewall rules exist for all open ports (Automated)", "yellow"))
        print(colored("Automated check for specific open port rules is complex. Manually review ip6tables rules.", "cyan"))
    else:
        print(colored("❌ iptables is NOT installed.", "red"))

# def check_permissions(file_path, expected_mode):
#     try:
#         st = os.stat(file_path)
#         actual_mode = stat.S_IMODE(st.st_mode)
#         return oct(actual_mode) == expected_mode, oct(actual_mode)
#     except FileNotFoundError:
#         return False, "File not found"

# def check_sshd_config(setting, expected_value):
#     try:
#         with open('/etc/ssh/sshd_config', 'r') as f:
#             lines = f.readlines()
#             for line in lines:
#                 if line.strip().startswith(setting):
#                     actual_value = line.split()[1]
#                     return actual_value == expected_value, actual_value
#         return False, "Not set"
#     except FileNotFoundError:
#         return False, "File not found"

# def check_cis_ssh():
#     results = {
#         "/etc/ssh/sshd_config permissions": check_permissions('sshd_config', '0o600'),
#         "SSH private key files": check_permissions('/etc/ssh/ssh_host_rsa_key', '0o600'),
#         "SSH public key files": check_permissions('/etc/ssh/ssh_host_rsa_key.pub', '0o644'),
#         "sshd access": check_sshd_config('AllowUsers', 'your_user'),
#         "sshd Banner": check_sshd_config('Banner', '/etc/issue.net'),
#         "sshd Ciphers": check_sshd_config('Ciphers', 'aes256-ctr,aes192-ctr,aes128-ctr'),
#         "ClientAliveInterval": check_sshd_config('ClientAliveInterval', '300'),
#         "DisableForwarding": check_sshd_config('DisableForwarding', 'yes'),
#         "GSSAPIAuthentication": check_sshd_config('GSSAPIAuthentication', 'no'),
#         "HostbasedAuthentication": check_sshd_config('HostbasedAuthentication', 'no'),
#         "IgnoreRhosts": check_sshd_config('IgnoreRhosts', 'yes'),
#         "KexAlgorithms": check_sshd_config('KexAlgorithms', 'diffie-hellman-group-exchange-sha256'),
#         "LoginGraceTime": check_sshd_config('LoginGraceTime', '60'),
#         "LogLevel": check_sshd_config('LogLevel', 'INFO'),
#         "MACs": check_sshd_config('MACs', 'hmac-sha2-512,hmac-sha2-256'),
#         "MaxAuthTries": check_sshd_config('MaxAuthTries', '4'),
#         "MaxSessions": check_sshd_config('MaxSessions', '10'),
#         "MaxStartups": check_sshd_config('MaxStartups', '10:30:60'),
#         "PermitEmptyPasswords": check_sshd_config('PermitEmptyPasswords', 'no'),
#         "PermitRootLogin": check_sshd_config('PermitRootLogin', 'no'),
#         "PermitUserEnvironment": check_sshd_config('PermitUserEnvironment', 'no'),
#         "UsePAM": check_sshd_config('UsePAM', 'yes')
#     }
    
#     for key, (status, actual) in results.items():
#         if status:
#             print(colored(f"✅ {key} (Automated): Pass", "green"))
#         else:
#             print(colored(f"⚠️ {key} (Automated): Fail - Actual: {actual}", "yellow"))

# def check_sudo_installed():
#     return os.system("which sudo > /dev/null 2>&1") == 0

# def check_sudo_pty():
#     with open("/etc/sudoers", "r") as f:
#         return any("Defaults use_pty" in line for line in f)

# def check_sudo_logfile():
#     with open("/etc/sudoers", "r") as f:
#         return any("Defaults logfile" in line for line in f)

# def check_sudo_requires_password():
#     with open("/etc/sudoers", "r") as f:
#         return not any("NOPASSWD" in line for line in f if not line.strip().startswith("#"))

# def check_sudo_reauth_not_disabled():
#     with open("/etc/sudoers", "r") as f:
#         return not any("!authenticate" in line for line in f if not line.strip().startswith("#"))

# def check_sudo_timeout():
#     with open("/etc/sudoers", "r") as f:
#         return any("timestamp_timeout" in line for line in f)

# def check_su_restricted():
#     result = subprocess.run(["grep", "pam_wheel.so", "/etc/pam.d/su"], capture_output=True, text=True)
#     return "required" in result.stdout

# def Configure_privilege_escalation():
#     print(f"5.2.1 Sudo installed: {'PASS' if check_sudo_installed() else 'FAIL'}")
#     print(f"5.2.2 Sudo commands use PTY: {'PASS' if check_sudo_pty() else 'FAIL'}")
#     print(f"5.2.3 Sudo log file exists: {'PASS' if check_sudo_logfile() else 'FAIL'}")
#     print(f"5.2.4 Sudo requires password: {'PASS' if check_sudo_requires_password() else 'FAIL'}")
#     print(f"5.2.5 Sudo re-authentication not disabled: {'PASS' if check_sudo_reauth_not_disabled() else 'FAIL'}")
#     print(f"5.2.6 Sudo timeout configured: {'PASS' if check_sudo_timeout() else 'FAIL'}")
#     print(f"5.2.7 SU access restricted: {'PASS' if check_su_restricted() else 'FAIL'}")

def check_package(package_name):
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

def Configure_PAM_software_packages():
    packages = ["pam", "libpam-modules", "libpam-pwquality"]
    for package in packages:
        check_package(package)

def check_pam_module(module_name):
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

def Configure_pam_auth_update_profiles(): 
    pam_modules = ["pam_unix", "pam_faillock", "pam_pwquality", "pam_pwhistory"]
    for module in pam_modules:
        check_pam_module(module)

def check_faillock_settings():
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

def check_pwhistory_settings():
    settings = {
        "remember": "5",
        "use_authtok": "yes"
    }
    
    try:
        with open("/etc/security/pwhistory.conf", "r") as f:
            content = f.read()
            
            for key, expected_value in settings.items():
                if key in content and expected_value in content:
                    print(colored(f"✔️ {key} is set to {expected_value}.", "green"))
                else:
                    print(colored(f"❌ {key} is NOT correctly set.", "red"))
    except Exception as e:
        print(colored(f"⚠️ Error checking pwhistory settings: {e}", "yellow"))

def check_pam_unix_settings():
    settings = {
        "nullok": "not present",
        "remember": "not present",
        "sha512": "present",
        "use_authtok": "present"
    }
    
    try:
        with open("/etc/pam.d/common-password", "r") as f:
            content = f.read()
            
            for key, expected_value in settings.items():
                if (expected_value == "not present" and key not in content) or (expected_value == "present" and key in content):
                    print(colored(f"✔️ {key} is correctly set.", "green"))
                else:
                    print(colored(f"❌ {key} is NOT correctly set.", "red"))
    except Exception as e:
        print(colored(f"⚠️ Error checking pam_unix settings: {e}", "yellow"))

def check_shadow_password_settings():
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

def check_last_password_change():
    try:
        result = subprocess.run(["chage", "-l", "$USER"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "Last password change" in result.stdout:
            print(colored(f"✔️ User's last password change date is set.", "green"))
        else:
            print(colored(f"❌ Last password change date is NOT set correctly.", "red"))
    except Exception as e:
        print(colored(f"⚠️ Error checking last password change: {e}", "yellow"))

def check_root_and_system_accounts():
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

