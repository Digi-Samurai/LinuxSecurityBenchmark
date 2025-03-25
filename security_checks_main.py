# security_checks_main.py
import subprocess
from termcolor import colored
from security_checks_utils import (
    run_check,
    check_module,
    check_partition,
    check_mount_options,
    InitialSetup_config,
    Server_Services_Check,
    Client_Services_Check,
    check_time_sync,
    check_cron_enabled,
    check_cron_permissions,
    check_crontab_restricted,
    check_at_restricted,
    check_cron_config,
    check_ipv6_status,
    check_wireless_disabled,
    check_bluetooth_inactive,
    check_kernel_modules,
    check_network_parameters,
    check_single_firewall,
    check_ufw,
    check_nftables,
    check_iptables,
    # check_cis_ssh,
    # Configure_privilege_escalation,
    Configure_PAM_software_packages,
    Configure_pam_auth_update_profiles,
    check_faillock_settings,
    check_pwquality_settings,
    check_pwhistory_settings,
    check_pam_unix_settings,
    check_shadow_password_settings,
    check_last_password_change,
    check_root_and_system_accounts
)
import os
import stat

kernel_modules = [
    "cramfs", "freevxfs", "hfs", "hfsplus", "jffs2",
    "overlay", "squashfs", "udf", "usb-storage"
]
partition_checks = {
    "/tmp": ["nodev", "nosuid", "noexec"],
    "/dev/shm": ["nodev", "nosuid", "noexec"],
    "/home": ["nodev", "nosuid"],
    "/var": ["nodev", "nosuid"],
    "/var/tmp": ["nodev", "nosuid", "noexec"],
    "/var/log": ["nodev", "nosuid", "noexec"],
    "/var/log/audit": ["nodev", "nosuid", "noexec"]
}
system_checks = {
    "AppArmor Installed": "dpkg -l | grep -i apparmor",
    "AppArmor Enabled": "aa-status",
    "Bootloader Password": "grep -i password /boot/grub/grub.cfg",
    "ASLR Enabled": "sysctl kernel.randomize_va_space",
    "Ptrace Scope Restricted": "sysctl kernel.yama.ptrace_scope",
    "Core Dumps Restricted": "grep -i 'hard core' /etc/security/limits.conf",
}
package_checks = {
    "GPG Keys Configured": "apt-key list",
    "Repositories Configured": "grep -r 'deb ' /etc/apt/sources.list*",
    "Security Updates Installed": "apt list --installed | grep -i security"
}
gdm_checks = {
    "GDM Removed": "dpkg -l | grep -i gdm",
    "GDM Login Banner": "grep -i banner /etc/gdm3/greeter.dconf-defaults",
    "GDM Screen Lock Enabled": "gsettings get org.gnome.desktop.screensaver lock-enabled",
    "XDMCP Disabled": "grep -i 'Enable=' /etc/gdm3/custom.conf"
}
banner_checks = {
    "Message of the Day (MOTD) Configured": "ls -l /etc/motd",
    "Local Login Warning Banner": "grep -i 'authorized' /etc/issue",
    "Remote Login Warning Banner": "grep -i 'authorized' /etc/issue.net",
    "Access to /etc/motd": "ls -l /etc/motd",
    "Access to /etc/issue": "ls -l /etc/issue",
    "Access to /etc/issue.net": "ls -l /etc/issue.net"
}
server_services = {
    "autofs": "systemctl is-active autofs",
    "avahi-daemon": "systemctl is-active avahi-daemon",
    "dhcpd": "systemctl is-active isc-dhcp-server",
    "named": "systemctl is-active named",
    "dnsmasq": "systemctl is-active dnsmasq",
    "vsftpd": "systemctl is-active vsftpd",
    "slapd": "systemctl is-active slapd",
    "dovecot": "systemctl is-active dovecot",
    "nfs-server": "systemctl is-active nfs-server",
    "nis": "systemctl is-active ypserv",
    "cups": "systemctl is-active cups",
    "rpcbind": "systemctl is-active rpcbind",
    "rsync": "systemctl is-active rsync",
    "smb": "systemctl is-active smbd",
    "snmpd": "systemctl is-active snmpd",
    "tftp": "systemctl is-active tftpd-hpa",
    "squid": "systemctl is-active squid",
    "apache2": "systemctl is-active apache2",
    "xinetd": "systemctl is-active xinetd",
    "xorg": "systemctl is-active xorg",
    "postfix": "systemctl is-active postfix",
    "cron": "systemctl is-active cron"
}
client_services = {
    "NIS Client": "dpkg -l | grep -i nis",
    "rsh Client": "dpkg -l | grep -i rsh-client",
    "talk Client": "dpkg -l | grep -i talk",
    "telnet Client": "dpkg -l | grep -i telnet",
    "LDAP Client": "dpkg -l | grep -i ldap-utils",
    "FTP Client": "dpkg -l | grep -i ftp"
}
time_services = {
    "check": "systemctl is-active systemd-timesyncd",
    "config": "grep -E '^NTP=' /etc/systemd/timesyncd.conf",
    "user_check": None
}
chrony_services = {
    "check": "systemctl is-active chronyd",
    "config": "grep -E '^server ' /etc/chrony/chrony.conf",
    "user_check": "ps -eo user,comm | grep '[c]hronyd'"
}
def Main_checks():
    sections = [
        ("Configure Filesystem Kernel Modules", "Checking Kernel Modules", kernel_modules, check_module),
        ("Configure Filesystem Partitions", "Checking Partitions", partition_checks.keys(), check_partition),
        ("Configure Filesystem Partitions", "Checking Mount Options", partition_checks.items(), check_mount_options),
        ("Package Management", "Checking Package Configurations", package_checks.items(), InitialSetup_config),
        ("Mandatory Access Control", "Checking AppArmor", [(k, v) for k, v in system_checks.items() if "AppArmor" in k], InitialSetup_config),
        ("Bootloader Configuration", "Checking Bootloader", [(k, v) for k, v in system_checks.items() if "Bootloader" in k], InitialSetup_config),
        ("Process Hardening", "Checking Process Hardening", [(k, v) for k, v in system_checks.items() if "ASLR" in k or "Ptrace" in k or "Core Dumps" in k], InitialSetup_config),
        ("GNOME Display Manager Configuration", "Checking GDM Configuration", gdm_checks.items(), InitialSetup_config),
        ("Login Banners & MOTD", "Checking Login Banner & MOTD Configuration", banner_checks.items(), InitialSetup_config),
        ("Configure Server Services", "Checking Server Services Configuration", server_services.items(), Server_Services_Check),
        ("Client Services Configuration", "Checking Unwanted Client Services", client_services.items(), Client_Services_Check),
        ("Host Based Firewall", "Checking Firewall Configuration", [], check_single_firewall)
    ]
    for title, subtitle, items, check_func in sections:
        print(colored("\n=========================================", "yellow", attrs=["bold"]))
        print(colored(f"🔹 {title} 🔹", "yellow", attrs=["bold"]))
        print(colored("=========================================\n", "yellow", attrs=["bold"]))
        print(colored(f"🔍 {subtitle}:", "cyan", attrs=["bold"]))
        for item in items:
            if isinstance(item, tuple):
                check_func(*item)
            else:
                check_func(item)
    print(colored("\n=========================================", "yellow", attrs=["bold"]))
    print(colored("🔹 Time Synchronization Check 🔹", "yellow", attrs=["bold"]))
    print(colored("=========================================\n", "yellow", attrs=["bold"]))
    check_time_sync(time_services, chrony_services)
    print(colored("\n=========================================", "yellow", attrs=["bold"]))
    print(colored("🔹 Configure Cron 🔹", "yellow", attrs=["bold"]))
    print(colored("=========================================\n", "yellow", attrs=["bold"]))
    check_cron_enabled()
    check_cron_config()
    check_crontab_restricted()
    print(colored("\n=========================================", "yellow", attrs=["bold"]))
    print(colored("🔹 Configure 'at' 🔹", "yellow", attrs=["bold"]))
    print(colored("=========================================\n", "yellow", attrs=["bold"]))
    check_at_restricted()
    print(colored("\n=========================================", "yellow", attrs=["bold"]))
    print(colored("🔹 Network Checks 🔹", "yellow", attrs=["bold"]))
    print(colored("=========================================\n", "yellow", attrs=["bold"]))
    check_ipv6_status()
    check_wireless_disabled()
    check_bluetooth_inactive()
    check_kernel_modules()
    check_network_parameters()
    print(colored("\n=========================================", "yellow", attrs=["bold"]))
    print(colored("🔹 Firewall Details 🔹", "yellow", attrs=["bold"]))
    print(colored("=========================================\n", "yellow", attrs=["bold"]))
    check_ufw()
    check_nftables()
    check_iptables()
    # print(colored("\n=========================================", "yellow", attrs=["bold"]))
    # print(colored("🔹 Configure SSH Server 🔹", "yellow", attrs=["bold"]))
    # print(colored("=========================================\n", "yellow", attrs=["bold"]))
    # check_cis_ssh()
    print(colored("\n=========================================", "yellow", attrs=["bold"]))
    print(colored("🔹 Configure PAM software packages 🔹", "yellow", attrs=["bold"]))
    print(colored("=========================================\n", "yellow", attrs=["bold"]))
    Configure_PAM_software_packages()
    print(colored("\n=========================================", "yellow", attrs=["bold"]))
    print(colored("🔹 Configure pam-auth-update profiles 🔹", "yellow", attrs=["bold"]))
    print(colored("=========================================\n", "yellow", attrs=["bold"]))
    Configure_pam_auth_update_profiles()
    print(colored("\n=========================================", "yellow", attrs=["bold"]))
    print(colored("🔹 Configure pam_faillock module 🔹", "yellow", attrs=["bold"]))
    print(colored("=========================================\n", "yellow", attrs=["bold"]))
    check_faillock_settings()
    print(colored("\n=========================================", "yellow", attrs=["bold"]))
    print(colored("🔹 Configure pam_pwquality module 🔹", "yellow", attrs=["bold"]))
    print(colored("=========================================\n", "yellow", attrs=["bold"]))
    check_pwquality_settings()
    print(colored("\n=========================================", "yellow", attrs=["bold"]))
    print(colored("🔹 Configure pam_pwhistory module 🔹", "yellow", attrs=["bold"]))
    print(colored("=========================================\n", "yellow", attrs=["bold"]))
    check_pwhistory_settings()
    print(colored("\n=========================================", "yellow", attrs=["bold"]))
    print(colored("🔹 Configure pam_unix module 🔹", "yellow", attrs=["bold"]))
    print(colored("=========================================\n", "yellow", attrs=["bold"]))
    check_pam_unix_settings()
    print(colored("\n=========================================", "yellow", attrs=["bold"]))
    print(colored("🔹 Configure shadow password suite parameters 🔹", "yellow", attrs=["bold"]))
    print(colored("=========================================\n", "yellow", attrs=["bold"]))
    check_shadow_password_settings()
    check_last_password_change()
    print(colored("\n=========================================", "yellow", attrs=["bold"]))
    print(colored("🔹 Configure root and system accounts and environment 🔹", "yellow", attrs=["bold"]))
    print(colored("=========================================\n", "yellow", attrs=["bold"]))
    check_root_and_system_accounts()

if __name__ == "__main__":
    Main_checks()