#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only acceptance checks for a newly installed AikaOS VM (run as root)."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import pwd
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--user', required=True, help='The account created by the installer')
args = parser.parse_args()
if os.geteuid() != 0:
    parser.error('Run as root to inspect account and service state.')
account = pwd.getpwnam(args.user)
checks = {}


def command(*argv):
    result = subprocess.run(argv, text=True, capture_output=True, check=False)
    return {'exit': result.returncode, 'stdout': result.stdout.strip(), 'stderr': result.stderr.strip()}


checks['installation_complete'] = Path('/var/lib/aikaos/installation-state').read_text().strip() == 'complete'
checks['installed_disk_boot'] = 'archisobasedir=' not in Path('/proc/cmdline').read_text()
checks['root_locked'] = command('passwd', '-S', 'root')['stdout'].split()[1] == 'L'
checks['user_password_set'] = command('passwd', '-S', args.user)['stdout'].split()[1] == 'P'
checks['sudo_requires_authentication'] = command('runuser', '-u', args.user, '--', 'sudo', '-n', '-k', 'true')['exit'] != 0
checks['single_normal_user'] = [p.pw_name for p in pwd.getpwall() if 1000 <= p.pw_uid < 65534] == [args.user]
checks['user_home_private'] = Path(account.pw_dir).stat().st_mode & 0o777 == 0o700
checks['sddm_avatar_present'] = Path(f'/usr/share/sddm/faces/{args.user}.face.icon').is_file()
checks['live_defaults_removed'] = not any(Path(p).exists() for p in (
    '/etc/sudoers.d/10-aika-live', '/etc/sddm.conf.d/10-aikaos.conf',
    '/etc/ssh/sshd_config.d/10-archiso.conf',
    '/etc/systemd/logind.conf.d/do-not-suspend.conf',
    '/etc/systemd/journald.conf.d/volatile-storage.conf',
))
checks['live_login_hint_removed'] = 'Live' not in Path('/etc/motd').read_text() and 'sudo ohne Passwort' not in Path('/etc/motd').read_text()
checks['installer_removed'] = command('pacman', '-Q', 'calamares')['exit'] != 0 and not Path('/usr/local/bin/install-aikaos').exists()
checks['boot_files_present'] = all(Path(p).is_file() and Path(p).stat().st_size > 0 for p in (
    '/boot/vmlinuz-linux', '/boot/initramfs-linux.img', '/boot/grub/grub.cfg',
))
checks['grub_aika_theme'] = 'GRUB_THEME="/usr/share/grub/themes/aikaos/theme.txt"' in Path('/etc/default/grub').read_text()
checks['aika_identity'] = 'ID=aikaos' in Path('/etc/os-release').read_text()
checks['fastfetch_config_preserved'] = hashlib.sha256(Path('/etc/xdg/fastfetch/config.jsonc').read_bytes()).hexdigest() == '7a76b5bb226248b4f36b5dec4d2fbac652825635afb837225e4037a698dbe848'
checks['arch_logo_alias_is_aika'] = Path('/usr/share/pixmaps/archlinux-logo.png').read_bytes() == Path('/usr/share/pixmaps/aikaos-logo.png').read_bytes()
checks['user_autolock_enabled'] = 'Autolock=true' in (Path(account.pw_dir) / '.config/kscreenlockerrc').read_text()
checks['no_build_repository'] = 'aikaos-build' not in Path('/etc/pacman.conf').read_text()
checks['expected_services_enabled'] = all(command('systemctl', 'is-enabled', unit)['stdout'] == 'enabled' for unit in (
    'NetworkManager.service', 'systemd-resolved.service', 'systemd-timesyncd.service', 'sddm.service',
))
checks['sshd_disabled'] = command('systemctl', 'is-enabled', 'sshd.service')['stdout'] == 'disabled'
system_failed = command('systemctl', '--failed', '--plain', '--no-legend')
user_env = ['runuser', '-u', args.user, '--', 'env', f'XDG_RUNTIME_DIR=/run/user/{account.pw_uid}', f'DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/{account.pw_uid}/bus']
user_failed = command(*user_env, 'systemctl', '--user', '--failed', '--plain', '--no-legend')
checks['no_failed_system_services'] = system_failed['exit'] == 0 and not system_failed['stdout']
checks['no_failed_user_services'] = user_failed['exit'] == 0 and not user_failed['stdout']
cores = command('coredumpctl', '--no-pager', '--no-legend', 'list')
checks['no_coredumps'] = cores['exit'] in (0, 1) and not cores['stdout']
report = {
    'checks': checks,
    'system_failed': system_failed,
    'user_failed': user_failed,
    'coredumps': cores,
    'root_mount': command('findmnt', '-n', '-o', 'SOURCE,FSTYPE', '/'),
    'kernel': os.uname().release,
    'machine_id': Path('/etc/machine-id').read_text().strip(),
    'package_keyring_has_private_key': any(Path('/etc/pacman.d/gnupg/private-keys-v1.d').glob('*.key')),
    'sudo_policy': command('sudo', '-l', '-U', args.user),
}
print(json.dumps(report, indent=2))
sys.exit(0 if all(checks.values()) else 1)
